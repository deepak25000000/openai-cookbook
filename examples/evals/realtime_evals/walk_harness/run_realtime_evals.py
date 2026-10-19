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
 from shared.result_types import (
@@
 )
+from shared.path_utils import safe_join, validate_example_id
@@
-def resolve_audio_path(audio_path_value: str, dataset_path: Path) -> Path:
-    if not audio_path_value:
-        raise ValueError("audio_path is empty")
-    audio_path = Path(audio_path_value)
-    if not audio_path.is_absolute():
-        audio_path = dataset_path.parent / audio_path
-    return audio_path
+def resolve_audio_path(audio_path_value: str, dataset_path: Path) -> Path:
+    if not audio_path_value:
+        raise ValueError("audio_path is empty")
+    # Use safe_join to prevent path traversal from CSV audio_path values
+    return safe_join(dataset_path.parent, audio_path_value)
@@
 def build_failed_result(
     row: pd.Series,
     dataset_path: Path,
     events_dir: Path,
     error_info: EvalErrorInfo,
 ) -> WalkEvalResult:
     example_id = str(row["example_id"])
+    validate_example_id(example_id)
     user_text = str(row["user_text"])
@@
 async def run_single_eval(
@@
     example_id = str(row["example_id"])
+    validate_example_id(example_id)
     user_text = str(row["user_text"])
@@
     audio_path = resolve_audio_path(str(row["audio_path"]), dataset_path)
@@
     if output_audio_bytes:
-        example_audio_dir = run_audio_dir / example_id
+        example_audio_dir = run_audio_dir / example_id
         ensure_dir(example_audio_dir)
         output_audio_path = example_audio_dir / "output.wav"
