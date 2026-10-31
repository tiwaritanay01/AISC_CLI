#include <stdio.h>
#include <stdbool.h>

void simulate_gobackn(int total_frames, int window_size) {
    int base = 1;
    int next_seq_num = 1;
    int simulated_drop_frame = 3; // Simulate loss of frame 3 on first try
    bool dropped_once = false;

    printf("Starting Go-Back-N Simulation (Total: %d frames, Window Size: %d)\n\n",
           total_frames, window_size);

    while (base <= total_frames) {
        // Send all frames in current window
        while (next_seq_num < base + window_size && next_seq_num <= total_frames) {
            printf("[Sender] Transmitting Frame %d\n", next_seq_num);
            next_seq_num++;
        }

        // Simulate ACKs
        for (int f = base; f < next_seq_num; f++) {
            if (f == simulated_drop_frame && !dropped_once) {
                printf("[Network] *** Frame %d LOST in transit! ***\n", f);
                printf("[Sender] Timeout expired for Frame %d! Sliding back window.\n", f);
                dropped_once = true;
                next_seq_num = f; // Go back to lost frame
                break;
            } else {
                printf("[Receiver] Frame %d received correctly -> Sending ACK %d\n", f, f);
                printf("[Sender] Received ACK %d -> Window advances\n", f);
                base++;
            }
        }
        printf("--------------------------------------------------\n");
    }
    printf("SUCCESS: All %d frames transmitted and acknowledged!\n", total_frames);
}

int main(void) {
    printf("==================================================\n");
    printf(" LabX Experiment 05: Sliding Window Protocol (GBN)\n");
    printf("==================================================\n");
    simulate_gobackn(6, 3);
    printf("==================================================\n");
    return 0;
}
