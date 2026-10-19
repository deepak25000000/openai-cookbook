@@
-from run_harness.run_realtime_evals import (
-    load_simulation,
-    load_simulation_index,
-    resolve_path,
-)
+from run_harness.run_realtime_evals import (
+    load_simulation,
+    load_simulation_index,
+    resolve_path,
+)
+from shared.path_utils import validate_example_id
@@
 def validate_crawl_input(data_path: Path) -> None:
     dataset = load_crawl_dataset(data_path)
+    # Ensure example_id values are safe identifiers
+    for row_index, row in dataset.iterrows():
+        example_id = str(row.get("example_id", "")).strip()
+        validate_example_id(example_id)
     _validate_expected_tool_arg_json(dataset, data_path)
@@
 def validate_walk_input(data_path: Path) -> None:
     dataset = load_walk_dataset(data_path)
+    # Ensure example_id values are safe identifiers
+    for row_index, row in dataset.iterrows():
+        example_id = str(row.get("example_id", "")).strip()
+        validate_example_id(example_id)
     _validate_expected_tool_arg_json(dataset, data_path)
     for row_index, row in dataset.iterrows():
         audio_path_value = str(row.get("audio_path", "")).strip()
@@
 def validate_run_input(data_path: Path) -> None:
     simulation_index = load_simulation_index(data_path)
@@
     for row_index, row in simulation_index.iterrows():
         simulation_id = str(row["simulation_id"]).strip()
+        # validate the simulation id used as a filename
+        validate_example_id(simulation_id)
         simulation_path = resolve_path(str(row["simulation_path"]), data_path.parent)
