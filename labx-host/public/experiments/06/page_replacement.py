"""Experiment 06: FIFO and LRU Page Replacement Simulation in Python."""

def simulate_fifo(reference_string: list[int], frame_count: int) -> int:
    frames = []
    faults = 0
    for page in reference_string:
        if page not in frames:
            faults += 1
            if len(frames) >= frame_count:
                frames.pop(0)
            frames.append(page)
    return faults

def simulate_lru(reference_string: list[int], frame_count: int) -> int:
    frames = []
    faults = 0
    for page in reference_string:
        if page in frames:
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            if len(frames) >= frame_count:
                frames.pop(0)
            frames.append(page)
    return faults

def main():
    print("=" * 55)
    print(" LabX Experiment 06: Page Replacement Simulation")
    print("=" * 55)
    
    reference = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frames = 3
    print(f"Page Reference String ({len(reference)} requests): {reference}")
    print(f"Available Physical Frame Capacity: {frames}\n")
    
    fifo_faults = simulate_fifo(reference, frames)
    lru_faults = simulate_lru(reference, frames)
    
    print(f"FIFO Algorithm : {fifo_faults} page faults (Hit Rate: {((len(reference)-fifo_faults)/len(reference))*100:.1f}%)")
    print(f"LRU  Algorithm : {lru_faults} page faults (Hit Rate: {((len(reference)-lru_faults)/len(reference))*100:.1f}%)")
    print("=" * 55)

if __name__ == "__main__":
    main()
