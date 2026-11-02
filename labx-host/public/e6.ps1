# LabX Remote: ERTOS Exp 06 (Code + Outputs)
$filename = "freertos_semaphores.ino"
$code = @'
/*
 * Experiment 18: Binary and Counting Semaphores for Task Synchronization in FreeRTOS
 * Demonstrates xSemaphoreCreateBinary and xSemaphoreCreateCounting on Arduino / AVR
 */

#include <Arduino_FreeRTOS.h>
#include <semphr.h>

SemaphoreHandle_t xBinarySemaphore;
SemaphoreHandle_t xCountingSemaphore;

void TaskProducer(void *pvParameters) {
    (void) pvParameters;
    int eventCount = 0;
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1500));
        eventCount++;
        Serial.print("[Producer] Signaling Binary Event #");
        Serial.println(eventCount);
        xSemaphoreGive(xBinarySemaphore);

        // Also give counting token if space allows
        xSemaphoreGive(xCountingSemaphore);
    }
}

void TaskBinaryConsumer(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        if (xSemaphoreTake(xBinarySemaphore, portMAX_DELAY) == pdTRUE) {
            Serial.println("  --> [Binary Consumer] Acquired semaphore! Synchronized task executed.");
        }
    }
}

void TaskCountingWorker(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        if (xSemaphoreTake(xCountingSemaphore, pdMS_TO_TICKS(3000)) == pdTRUE) {
            Serial.println("  --> [Counting Worker] Shared resource accessed (Token acquired).");
            vTaskDelay(pdMS_TO_TICKS(400));
        } else {
            Serial.println("  --> [Counting Worker] Resource wait timeout.");
        }
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Binary & Counting Semaphore Demo ===");

    xBinarySemaphore = xSemaphoreCreateBinary();
    xCountingSemaphore = xSemaphoreCreateCounting(3, 0);

    if (xBinarySemaphore != NULL && xCountingSemaphore != NULL) {
        xTaskCreate(TaskProducer, "Producer", 128, NULL, 2, NULL);
        xTaskCreate(TaskBinaryConsumer, "BinConsumer", 128, NULL, 1, NULL);
        xTaskCreate(TaskCountingWorker, "CountWorker", 128, NULL, 1, NULL);
    }
}

void loop() {
    // Empty: FreeRTOS scheduler manages execution
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
FreeRTOS is a lightweight open source Real time Operating system (RTOS)
made for use in embedded systems. It helps manage multiple tasks schedules
them properly allows tasks to work together smoothly and share resources
without conflict. Semaphores are synchronization mechanisms used to
coordinate tasks. A Binary Semaphore has a maximum count of 1, functioning
similarly to a mutex flag to signal events between tasks or ISRs using
xSemaphoreCreateBinary, xSemaphoreTake, and xSemaphoreGive. A Counting
Semaphore has a count >= 1 (xSemaphoreCreateCounting), tracking multiple
available units of a shared resource or counting events. When tasks take
the semaphore, the count decrements; when tasks release the resource, the
count increments.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp06_output.jpg"
try {
    Invoke-WebRequest "https://aisccli.netlify.app/outputs/ertos_exp06_output.jpg" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp06_output.jpg" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp06_output.jpg: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp06_output.pdf"
try {
    Invoke-WebRequest "https://aisccli.netlify.app/outputs/ertos_exp06_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp06_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp06_output.pdf: $_" -ForegroundColor DarkGray
}