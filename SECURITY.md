# Security and privacy

Pre-alpha review scaffold. No production-security, compliance, or document-safety certification.

The implemented CLI reads one local JSON declaration, validates it, and prints status JSON.
It does not read PDFs, run extractors, load plugins, open a network connection, or send telemetry.
It bounds JSON input to 1 MiB and expected-value nesting to 32 levels, rejects duplicate keys,
floating/non-finite JSON numbers, unsupported fields, and invalid declaration relationships.
These checks are input validation, not a process sandbox. Use regular local files from trusted sources;
blocking devices and operating-system resource isolation remain the caller's responsibility.

Do not put sensitive documents or model outputs into public issues. Report non-sensitive bugs with
synthetic reproductions. For a potentially exploitable security issue, use GitHub's private reporting
mechanism if available; otherwise request a private contact route without posting the exploit or data.
Private reporting has not been verified enabled in repository settings.

See [the threat model](docs/THREAT_MODEL.md) for planned controls and their limits.
