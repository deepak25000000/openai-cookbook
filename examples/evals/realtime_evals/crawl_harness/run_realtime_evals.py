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
+from shared.path_utils import validate_example_id
@@
 def build_failed_result(
     row: pd.Series,
     run_audio_dir: Path,
     run_events_dir: Path,
     error_info: EvalErrorInfo,
 ) -> CrawlEvalResult:
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
     example_audio_dir = run_audio_dir / example_id
     ensure_dir(example_audio_dir)
