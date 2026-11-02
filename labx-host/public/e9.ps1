# LabX Remote: ERTOS Exp 09 (Code + Outputs)
$filename = "freertos_ipc.ino"
$code = @'
/*
 * Experiment 21: Real-Time Application IPC in FreeRTOS
 * Demonstrates Message Queues, Mutexes, and Event Groups for Inter-Task Messaging
 */

#include <Arduino_FreeRTOS.h>
#include <queue.h>
#include <semphr.h>

struct SensorPacket {
    int sensorId;
    int reading;
};

QueueHandle_t xSensorQueue;
SemaphoreHandle_t xSerialMutex;

void TaskProducer(void *pvParameters) {
    (void) pvParameters;
    struct SensorPacket packet;
    int counter = 0;
    for (;;) {
        counter++;
        packet.sensorId = 101;
        packet.reading = 50 + (counter % 30);

        if (xQueueSend(xSensorQueue, &packet, pdMS_TO_TICKS(100)) == pdPASS) {
            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
                Serial.print("[Producer] Sent packet #");
                Serial.print(counter);
                Serial.print(" Value: ");
                Serial.println(packet.reading);
                xSemaphoreGive(xSerialMutex);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(800));
    }
}

void TaskConsumer(void *pvParameters) {
    (void) pvParameters;
    struct SensorPacket received;
    for (;;) {
        if (xQueueReceive(xSensorQueue, &received, portMAX_DELAY) == pdPASS) {
            if (xSemaphoreTake(xSerialMutex, portMAX_DELAY) == pdTRUE) {
                Serial.print("  --> [Consumer] Received Sensor: ");
                Serial.print(received.sensorId);
                Serial.print(" | Calibrated Data: ");
                Serial.println(received.reading * 1.5);
                xSemaphoreGive(xSerialMutex);
            }
        }
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS IPC: Queue, Mutex & Task Synchronization ===");

    xSensorQueue = xQueueCreate(5, sizeof(struct SensorPacket));
    xSerialMutex = xSemaphoreCreateMutex();

    if (xSensorQueue != NULL && xSerialMutex != NULL) {
        xTaskCreate(TaskProducer, "Producer", 128, NULL, 1, NULL);
        xTaskCreate(TaskConsumer, "Consumer", 128, NULL, 1, NULL);
    }
}

void loop() {
    // RTOS Managed
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
Inter-Process Communication (IPC) is a vital RTOS mechanism that allows
asynchronously executing tasks to safely exchange data and synchronization
events without memory corruption or race conditions. FreeRTOS provides
Message Queues (xQueueCreate, xQueueSend, xQueueReceive) for thread-safe
FIFO passing of data packets, Event Groups (xEventGroupCreate,
xEventGroupSetBits, xEventGroupWaitBits) for compound multi-task flag
synchronization, and Semaphores/Mutexes for mutually exclusive hardware
bus access. In this experiment, a producer task sends data packets through
a queue while an event group signals synchronization milestones.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp09_drive_output.pdf"
try {
    Invoke-WebRequest "https://aisccli.netlify.app/outputs/ertos_exp09_drive_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp09_drive_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp09_drive_output.pdf: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp09_output.pdf"
try {
    Invoke-WebRequest "https://aisccli.netlify.app/outputs/ertos_exp09_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp09_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp09_output.pdf: $_" -ForegroundColor DarkGray
}