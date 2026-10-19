@@
-from shared.realtime_harness_utils import (
+from shared.realtime_harness_utils import (
     RealtimeResponseError,
     audio_format_config,
     collect_realtime_response,
     ensure_dir,
     stream_audio_to_connection,
     write_pcm16_wav,
 )
+from shared.path_utils import safe_join, validate_example_id
@@
-def resolve_path(path_value: str, base_dir: Path) -> Path:
-    if not path_value:
-        raise ValueError("Path value is empty")
-    candidate = Path(path_value)
-    if not candidate.is_absolute():
-        candidate = base_dir / candidate
-    return candidate
+def resolve_path(path_value: str, base_dir: Path) -> Path:
+    """Resolve a user-provided path_value against base_dir safely.
+
+    This disallows absolute paths and user expansion (~/$VAR). It resolves the
+    final path and ensures it stays inside base_dir.
+    """
+    if not path_value:
+        raise ValueError("Path value is empty")
+    return safe_join(base_dir, path_value)
@@
 def build_failed_simulation_result(
     simulation_row: pd.Series,
     args: argparse.Namespace,
     run_dir: Path,
     error_info: EvalErrorInfo,
 ) -> RunSimulationResult:
     simulation_id = str(simulation_row.get("simulation_id", "")).strip() or "unknown"
+    # Validate the simulation_id so it cannot be used to escape run directories.
+    validate_example_id(simulation_id)
     run_audio_dir = run_dir / "audio" / simulation_id
     trace_path = run_dir / "events" / f"{simulation_id}.jsonl"
@@
     simulation_id = simulation.get(
         "simulation_id", str(simulation_row["simulation_id"])
     )
+    # Validate simulation_id as a strict identifier (not a path)
+    validate_example_id(simulation_id)
     scenario = simulation.get("scenario", "")
@@
     run_audio_dir = run_dir / "audio" / simulation_id
     run_events_dir = run_dir / "events"
     run_conv_dir = run_dir / "conversations"
     ensure_dir(run_audio_dir)
     ensure_dir(run_events_dir)
     ensure_dir(run_conv_dir)
