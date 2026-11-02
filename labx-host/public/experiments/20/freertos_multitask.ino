/*
 * Experiment 20: Creating Multiple Tasks using FreeRTOS on Arduino UNO
 * Demonstrates Priority-Based Preemption and Task State Transitions
 */

#include <Arduino_FreeRTOS.h>

void TaskHighPriority(void *pvParameters) {
    (void) pvParameters;
    for (;;) {
        Serial.println(">>> [HIGH PRIORITY TASK - 3] Critical execution cycle started.");
        vTaskDelay(pdMS_TO_TICKS(2000));
    }
}

void TaskMediumPriority(void *pvParameters) {
    (void) pvParameters;
    int reading = 0;
    for (;;) {
        reading = analogRead(A0);
        Serial.print("  [MED PRIORITY TASK - 2] Telemetry Sensor A0: ");
        Serial.println(reading);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void TaskLowPriority(void *pvParameters) {
    (void) pvParameters;
    unsigned long count = 0;
    for (;;) {
        count++;
        Serial.print("    [LOW PRIORITY TASK - 1] Background heartbeat tick: ");
        Serial.println(count);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void setup() {
    Serial.begin(9600);
    while (!Serial) { ; }
    Serial.println("=== FreeRTOS Multiple Tasks & Preemption Demonstration ===");

    xTaskCreate(TaskLowPriority,    "LowTask",  128, NULL, 1, NULL);
    xTaskCreate(TaskMediumPriority, "MedTask",  128, NULL, 2, NULL);
    xTaskCreate(TaskHighPriority,   "HighTask", 128, NULL, 3, NULL);
}

void loop() {
    // Managed by RTOS
}

/*
============================================================================
EXPERIMENT THEORY (from Embedded Systems & RTOS Laboratory Submission):
============================================================================
Multitasking in FreeRTOS enables the concurrent execution of multiple
independent operational threads on a single core microcontroller. The
FreeRTOS preemptive scheduler enforces priority-based task switching,
ensuring that the highest priority ready task always gains execution
control. In this experiment, three distinct tasks (Sensor Reading Task,
Display/Telemetry Task, and Heartbeat Monitor Task) are instantiated with
varying priorities to demonstrate how priority inversion is avoided and
how tasks cleanly share CPU cycles.
============================================================================
*/
