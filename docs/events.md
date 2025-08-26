# Events (stub)
- `waitlist.joined` { business_id, list_id, entry_id, name, size, contact? }
- `waitlist.updated` { entry_id, status, position, eta_minutes }
- `notify.send` { channel: "telegram"|"sms", to, template, params }
