# Local PearlBook configuration

`scripts/setup_pearlbook.py` writes `local-config.md` for you. Copy this file by hand
only if you are not using the setup script. Do not commit the copied file.

```yaml
vault_name: YourVaultName
vault_path: /absolute/path/to/your/vault
access_mode: local
default_access: read_only
note_changes: explicit_request_only
link_style: obsidian        # obsidian (default) | path | https_bridge (opt-in)
# link_base: https://your-redirector.example/   # required only for https_bridge
```

Only authorize the vault itself and a dedicated workspace. Do not use a home directory or cloud-storage root as `vault_path`.

`https_bridge` makes note links clickable in chat renderers that ignore `obsidian://`
links, but the redirector receives the vault name and note path. `https://obsid.net/`
is a third-party service run by Joost de Valk, not by Obsidian; a self-hosted
redirector keeps that metadata private.
