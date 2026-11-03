# LabX Remote: ERTOS Exp 07 (Code + Outputs)
$filename = "freertos_porting.ino"
$code = @'
/*
 * Experiment 19: Porting FreeRTOS to Arduino UNO (ATmega328P) Development Board
 * Demonstrates Kernel Porting, Preemptive Task Scheduling & vTaskDelay()
 */

#include <Arduino_FreeRTOS.h>

#define LED_PIN_1 12
#define LED_PIN_2 13

void TaskBlink1(void *pvParameters) {
    (void) pvParameters;
    pinMode(LED_PIN_1, OUTPUT);
    for (;;) {
        digitalWrite(LED_PIN_1, HIGH);
        vTaskDelay(pdMS_TO_TICKS(250));
        digitalWrite(LED_PIN_1, LOW);
        vTaskDelay(pdMS_TO_TICKS(250));
        Serial.println("[Task 1] Fast Blink (250ms) - Priority 1");
    }
}

void TaskBlink2(void *pvParameters) {
    (void) pvParameters;
    pinMode(LED_PIN_2, OUTPUT);
    for (;;) {
        digitalWrite(LED_PIN_2, HIGH);
        vTaskDelay(pdMS_TO_TICKS(1000));
        digitalWrite(LED_PIN_2, LOW);
        vTaskDelay(pdMS_TO_TICKS(1000));
        Serial.println("[Task 2] Slow Heartbeat (1000ms) - Priority 1");
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Arduino Porting & Multitasking Initialized ===");

    xTaskCreate(TaskBlink1, "FastBlink", 128, NULL, 1, NULL);
    xTaskCreate(TaskBlink2, "SlowBlink", 128, NULL, 1, NULL);
}

void loop() {
    // Arduino loop stays empty; RTOS scheduler handles tasks
}



/* --- Line 50: Execution & Theory Division --- */

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
FreeRTOS is a lightweight real-time operating system designed for embedded
systems with constrained memory footprint. Porting FreeRTOS to the
ATmega328P microcontroller on the Arduino UNO board allows developers to
run preemptive priority-based multitasking on an 8-bit platform. The
FreeRTOS kernel replaces the traditional single-threaded loop() construct
with independent task routines, each possessing its own stack, priority,
and state machine. Tasks yield control cooperatively using vTaskDelay(),
allowing the scheduler to context-switch to ready tasks.
============================================================================
*/

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved code to: $filename (Theory embedded after line 50)" -ForegroundColor White

$outTarget = Join-Path $PWD "ertos_exp07_output.jpg"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp07_output.jpg" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp07_output.jpg" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp07_output.jpg: $_" -ForegroundColor DarkGray
}
$outTarget = Join-Path $PWD "ertos_exp07_output.pdf"
try {
    Invoke-WebRequest "https://cli-t0km.onrender.com/outputs/ertos_exp07_output.pdf" -OutFile $outTarget -UseBasicParsing
    Write-Host "[OK] Downloaded Output to: ertos_exp07_output.pdf" -ForegroundColor White
} catch {
    Write-Host "[!] Could not fetch ertos_exp07_output.pdf: $_" -ForegroundColor DarkGray
}