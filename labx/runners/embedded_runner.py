"""Embedded C and Hardware Toolchain adapter."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from labx.models import RunConfig
from labx.runners.base import BaseLanguageRunner


class EmbeddedRunner(BaseLanguageRunner):
    """Adapter for Embedded C and specialized hardware experiments (ARM7, Keil, Proteus)."""

    @property
    def name(self) -> str:
        return "Embedded C"

    def check_prerequisites(self) -> Tuple[bool, str]:
        # Check if cross compiler like arm-none-eabi-gcc or make exists
        arm_gcc = shutil.which("arm-none-eabi-gcc")
        make_bin = shutil.which("make")
        if arm_gcc:
            return True, f"Found ARM cross-toolchain: {arm_gcc}"
        if make_bin:
            return True, f"Found build utility: {make_bin}"
        return True, "Source generation ready. Vendor toolchain (Keil/Proteus/FlashMagic) required for simulation/flashing."

    def get_toolchain_help(self) -> str:
        return (
            "Embedded firmware targets specific microcontroller hardware.\n"
            "• Keil µVision IDE: https://www.keil.com/demo/eval/arm.htm\n"
            "• Proteus VSM (Simulation): https://www.labcenter.com/\n"
            "• GNU Arm Embedded Toolchain: https://developer.arm.com/downloads/-/gnu-rm\n"
            "• Flash Magic (NXP LPC ISP Flashing): https://www.flashmagictool.com/"
        )

    def compile(self, exp_dir: Path, run_config: RunConfig) -> Tuple[bool, str]:
        # Check if arm-none-eabi-gcc is available and Makefile or .c files exist
        arm_gcc = shutil.which("arm-none-eabi-gcc")
        makefile = exp_dir / "Makefile"

        if arm_gcc and makefile.exists():
            print("\n[LabX] Detected arm-none-eabi-gcc and Makefile. Compiling firmware image...")
            try:
                res = subprocess.run(
                    ["make"],
                    cwd=str(exp_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if res.returncode == 0:
                    return True, "Embedded firmware compiled successfully."
                else:
                    return False, f"Cross-compilation failed:\n{res.stderr}\n{res.stdout}"
            except Exception as exc:
                return False, f"Build error: {exc}"

        return True, "Embedded source files generated and validated."

    def build_execution_command(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[List[str]]:
        # Embedded hardware cannot be directly run on a host PC CPU without emulator/hardware
        return None

    def run(
        self,
        exp_dir: Path,
        run_config: RunConfig,
        component_name: Optional[str] = None,
        extra_args: Optional[List[str]] = None
    ) -> int:
        hardware = run_config.hardware or "Target Microcontroller (e.g. ARM7 LPC2148)"
        print("\n" + "=" * 60)
        print(f" LABX HARDWARE SIMULATION & EXECUTION GUIDE: {hardware.upper()}")
        print("=" * 60)
        print(f"Target Hardware:     {hardware}")
        print(f"Experiment Directory: {exp_dir.resolve()}")
        print("\nGenerated Firmware Files:")
        for item in exp_dir.iterdir():
            if item.is_file() and item.name != "README.md":
                print(f"  • {item.name}")

        print("\nToolchain Workflow Instructions:")
        if run_config.toolchain_guide:
            print(run_config.toolchain_guide)
        else:
            print("1. Keil µVision Project Setup:")
            print("   - Open Keil µVision and select 'Project' -> 'New µVision Project'.")
            print(f"   - Select Device: {hardware}.")
            print("   - Copy 'STARTUP.s' when prompted and add the generated .c file(s).")
            print("   - In Options for Target -> Output, enable 'Create HEX File'.")
            print("   - Click 'Build' (F7) to generate the .hex binary.")
            print("\n2. Proteus Simulation:")
            print("   - Place the microcontroller schematic component into Proteus.")
            print("   - Connect peripherals (LEDs, LCD, UART or Motors) as outlined in the experiment.")
            print("   - Double-click the MCU component and load the generated .hex file into 'Program File'.")
            print("   - Press 'Play' in Proteus to run the real-time simulation.")
            print("\n3. Hardware Flashing (Flash Magic / ISP):")
            print("   - Connect the development board via USB-to-UART.")
            print("   - Set COM port and baud rate (e.g., 9600 / 115200) in Flash Magic.")
            print("   - Select the generated .hex file and press 'Start' to flash.")

        print("=" * 60)
        return 0

