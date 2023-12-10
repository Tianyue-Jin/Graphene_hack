/*  WiFi softAP Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_mac.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"


// UDP/IP  Client Includes
#include "protocol_examples_common.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include <lwip/netdb.h>


// ADC 
#include "driver/gpio.h"
#include "driver/adc.h"
#include "esp_adc_cal.h"

/* The examples use WiFi configuration that you can set via project configuration menu.

   If you'd rather not, just change the below entries to strings with
   the config you want - ie #define EXAMPLE_WIFI_SSID "mywifissid"
*/
#define ESP_WIFI_SSID      "GROUP3WIFI"
#define ESP_WIFI_PASS      "letmein1234"
#define ESP_WIFI_CHANNEL   6
#define MAX_STA_CONN       1

static const char *TAG = "wifi softAP";

TaskHandle_t udpTaskH;
// **** SENSOR DAT PUBLSIHER *******
#define HOST_IP_ADDR "192.168.4.2"
#define PORT 12345

#define ADC_WIDTH_BIT 12 // ADC data width


void initialize_adc() {
    adc1_config_width(ADC_WIDTH_BIT_12); // Set ADC data width to 12 bits
    adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11); // Set attenuation of ADC input channel
}


float convert_to_voltage(int raw_value) {
    float voltage = (raw_value / (float)(1 << ADC_WIDTH_BIT)) * 3.3; // Convert raw ADC value to voltage
    return voltage;
}



void udpTask(void *pvParameters){
    bool running =false;

    int addr_family = 0;
    int ip_protocol = 0;
    struct sockaddr_in dest_addr;
        dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
        dest_addr.sin_family = AF_INET;
        dest_addr.sin_port = htons(PORT);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;

    int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            running = false;
        }
    running = true;
    // set timeout
    struct timeval timeout;
        timeout.tv_sec = 10;
        timeout.tv_usec = 0;
        setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);

    ESP_LOGI(TAG, "Socket created, sending to %s:%d", HOST_IP_ADDR, PORT);




    char buffer[20];
    float test;
    uint32_t adc_val;
    float val;
    while(running){
        test = ((float)rand() / RAND_MAX);
        adc_val = adc1_get_raw(ADC1_CHANNEL_0);
        val = convert_to_voltage(adc_val);
        
        sprintf(buffer, "%f:%f", val+0.5, val);
        int err = sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }
            ESP_LOGI(TAG, "Message sent %f\n", val);


        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
    if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket");
            shutdown(sock, 0);
            close(sock);
        }
        vTaskDelete(NULL);
}







// Notifies of wifi Connection events
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                    int32_t event_id, void* event_data)
{
    if (event_id == WIFI_EVENT_AP_STACONNECTED) {
        wifi_event_ap_staconnected_t* event = (wifi_event_ap_staconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" join, AID=%d",
                 MAC2STR(event->mac), event->aid);
        vTaskDelay(2000/ portTICK_PERIOD_MS);
        xTaskCreate(udpTask, "udp_client", 4096, NULL, 5, &udpTaskH);
    } else if (event_id == WIFI_EVENT_AP_STADISCONNECTED) {
        wifi_event_ap_stadisconnected_t* event = (wifi_event_ap_stadisconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" leave, AID=%d",
                 MAC2STR(event->mac), event->aid);
        vTaskDelete(udpTaskH);
    }
}

// Begins Soft access point
void wifi_init_softap(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_ap();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        NULL));

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = ESP_WIFI_SSID,
            .ssid_len = strlen(ESP_WIFI_SSID),
            .channel = ESP_WIFI_CHANNEL,
            .password = ESP_WIFI_PASS,
            .authmode = WIFI_AUTH_OPEN,
            .max_connection = MAX_STA_CONN,
            .pmf_cfg = {
                    .required = true,
            },
        },
    };
    if (strlen(ESP_WIFI_PASS) == 0) {
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "wifi_init_softap finished. SSID:%s password:%s channel:%d",
             ESP_WIFI_SSID, ESP_WIFI_PASS, ESP_WIFI_CHANNEL);
}


















void app_main(void)
{
    //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    
    // init adc
    initialize_adc();

    ESP_LOGI(TAG, "ESP_WIFI_MODE_AP");
    wifi_init_softap();

   
}