# zoo-template-common

Shared reusable classes for service templates used in the ZOO-Project CWL runner ecosystem.

This repository centralizes commonly used logic like execution handlers and STAC I/O utilities to avoid duplication and simplify maintenance across multiple service templates.

---

## Included Modules

| File | Description |
|------|-------------|
| `common_execution_handler.py` | Defines a base `ExecutionHandler` class with standard hook methods like `pre_execution_hook`, `post_execution_hook`, `handle_outputs`, etc. |
| `common_stac_io.py` | Implements `CustomStacIO` using `boto3` to support reading/writing STAC catalogs from/to S3. |

---

## How to Use in a Service Template

### 1. Import the Common Execution Handler

```python
from zoo_template_common.common_execution_handler import ExecutionHandler

class MyHandler(ExecutionHandler):
    def handle_outputs(self, log, output, usage_report, tool_logs):
        self.results = {"url": output["result_path"]}
```

You can override only the hooks you need:

```python
def get_pod_env_vars(self, **kwargs):
    return {"A": "1", "B": "2"}
```
### 2. Use the Custom STAC I/O Handler for S3
```python
from zoo_template_common.common_stac_io import CustomStacIO
from pystac.stac_io import StacIO

StacIO.set_default(CustomStacIO)
```
## Why Use This?
- Avoids duplicating handler and I/O logic across templates

- Centralizes updates and bug fixes

- Promotes extensibility using clean class inheritance

- Easily shareable across multiple ZOO service templates

## Repositories Using This
- zoo-service-template
- eoepca-proc-service-template
- zoo-argo-wf-proc-service-template
- eoepca-proc-service-template-wes

## Local Development & Installation

Add it to PYTHONPATH in your service.py:
```python
import sys, os
sys.path.append("/path/to/zoo-template-common")
```
