"""Data models for LabX experiment metadata, catalog, and run configurations."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any


@dataclass
class ExperimentFile:
    """Represents an individual file belonging to an experiment."""
    path: str
    source: str
    role: str = "source"  # "source", "header", "docs", "config", "data"


@dataclass
class ProcessConfig:
    """Configuration for an executable component/process."""
    name: str
    entry: str
    compile_cmd: Optional[List[str]] = None
    run_cmd: Optional[List[str]] = None
    args: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class RunConfig:
    """Execution parameters and compiler commands for an experiment."""
    kind: str  # "python", "java", "c", "cpp", "embedded_c"
    entry: str
    compile_cmd: Optional[List[str]] = None
    run_cmd: Optional[List[str]] = None
    compiler: Optional[str] = None
    runtime: Optional[str] = None
    hardware: Optional[str] = None
    toolchain_guide: Optional[str] = None
    components: Dict[str, ProcessConfig] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunConfig":
        components = {}
        if "components" in data and isinstance(data["components"], dict):
            for name, comp_data in data["components"].items():
                components[name] = ProcessConfig(
                    name=comp_data.get("name", name),
                    entry=comp_data.get("entry", ""),
                    compile_cmd=comp_data.get("compile_cmd"),
                    run_cmd=comp_data.get("run_cmd"),
                    args=comp_data.get("args", []),
                    description=comp_data.get("description", "")
                )
        return cls(
            kind=data.get("kind", "python"),
            entry=data.get("entry", ""),
            compile_cmd=data.get("compile_cmd"),
            run_cmd=data.get("run_cmd"),
            compiler=data.get("compiler"),
            runtime=data.get("runtime"),
            hardware=data.get("hardware"),
            toolchain_guide=data.get("toolchain_guide"),
            components=components
        )


@dataclass
class ExperimentManifest:
    """Complete metadata and file list for an individual experiment."""
    id: int
    slug: str
    title: str
    language: str
    aliases: List[str]
    description: str
    aim: str
    theory: str
    algorithm: List[str]
    files: List[ExperimentFile]
    run: RunConfig
    requirements: Optional[str] = None
    version: str = "1.0.0"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExperimentManifest":
        files = [
            ExperimentFile(
                path=f.get("path", ""),
                source=f.get("source", ""),
                role=f.get("role", "source")
            )
            for f in data.get("files", [])
        ]
        run_data = data.get("run", {})
        run_cfg = RunConfig.from_dict(run_data) if isinstance(run_data, dict) else RunConfig(kind="python", entry="")

        return cls(
            id=int(data["id"]),
            slug=data.get("slug", f"exp-{data['id']}"),
            title=data.get("title", f"Experiment {data['id']}"),
            language=data.get("language", "generic"),
            aliases=data.get("aliases", []),
            description=data.get("description", ""),
            aim=data.get("aim", ""),
            theory=data.get("theory", ""),
            algorithm=data.get("algorithm", []),
            files=files,
            run=run_cfg,
            requirements=data.get("requirements"),
            version=data.get("version", "1.0.0")
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CatalogItem:
    """Summary record for an experiment in the global catalogue."""
    id: int
    slug: str
    title: str
    language: str
    aliases: List[str]
    description: str
    manifest_url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CatalogItem":
        return cls(
            id=int(data["id"]),
            slug=data.get("slug", f"exp-{data['id']}"),
            title=data.get("title", f"Experiment {data['id']}"),
            language=data.get("language", "generic"),
            aliases=data.get("aliases", []),
            description=data.get("description", ""),
            manifest_url=data.get("manifest_url", f"experiments/{int(data['id']):02d}/manifest.json")
        )


@dataclass
class Catalog:
    """The complete experiment catalogue published on the remote host."""
    version: str
    updated_at: str
    experiments: List[CatalogItem]
    zip_url: str = "downloads/labx_experiments.zip"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Catalog":
        experiments = [CatalogItem.from_dict(item) for item in data.get("experiments", [])]
        return cls(
            version=data.get("version", "1.0.0"),
            updated_at=data.get("updated_at", ""),
            experiments=experiments,
            zip_url=data.get("zip_url", "downloads/labx_experiments.zip")
        )

    def get_by_id(self, exp_id: int) -> Optional[CatalogItem]:
        for item in self.experiments:
            if item.id == exp_id:
                return item
        return None

