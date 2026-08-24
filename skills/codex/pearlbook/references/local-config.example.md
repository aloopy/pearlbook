# Local PearlBook configuration

Copy this file to `local-config.md` inside the installed skill. Do not commit the copied file.

```yaml
vault_name: YourVaultName
vault_path: /absolute/path/to/your/vault
default_access: read_only
note_changes: explicit_request_only
link_style: obsid_net
link_base: https://obsid.net/
```

Only authorize the vault itself and a dedicated workspace. Do not use a home directory or cloud-storage root as `vault_path`.
