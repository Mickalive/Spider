---
description: Minimal free-model access check. No filesystem, subprocess, browser, network-tool or edit privileges.
mode: primary
permission:
  "*": deny
  read: deny
  bash: deny
  edit: deny
  question: deny
  external_directory: deny
---

You are a model availability probe. No tools. No reasoning narrative. Return exactly:
SPIDER_FREE_PROVIDER_READY
