# Attach Files to a Claude Desktop Project

When a guide needs files attached to a Claude Desktop Project, use the **Project Files panel**, not the chat paperclip.

## In a Project: use the + under Files

1. In the Project panel (right side of Claude Desktop), locate the **Files** section.
2. Click the **+** (plus) button next to Files.
3. In the menu that opens, click **Upload from device**.
4. In the file picker, paste the folder path into the **address bar** (not the filename field), press Enter.
5. Press **Ctrl+A** to select all files, click **Open**.
6. Wait for upload to complete. Files appear in the Project's Files list.

Files attached this way are available to every conversation inside the Project without re-attaching.

## Key mistake to avoid

Do NOT click the paperclip icon in the chat input area. That attaches files to a single message, not to the Project. In Project mode, always use the Files section in the right-side Project panel.

## Midscene prompt template

```text
npx midscene-computer act --prompt "In the Project panel on the right, click the + button next to Files, then click Upload from device. In the file picker, paste the folder path into the address bar, press Enter, press Ctrl+A to select all files, click Open."
```

## Native in-app browser equivalent

In the web app a Project exposes the same Files panel. Open the Project, click the **+** next to Files in the right panel, choose **Upload from device**, and pick the files. Uploads to a message (paperclip) still attach per-message, not to the Project, so the same rule holds.
