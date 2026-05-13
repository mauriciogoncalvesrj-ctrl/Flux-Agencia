# Google APIs & Scopes Supported by gog v0.16.0

Complete list from `gog auth services --json` on 2026-05-12.

| Service | User Auth | Scopes | APIs | Notes |
|---------|-----------|--------|------|-------|
| gmail | ✅ | gmail.modify, gmail.settings.basic, gmail.settings.sharing | Gmail API | |
| calendar | ✅ | calendar | Calendar API | |
| chat | ✅ | chat.spaces, chat.messages, chat.memberships, chat.users.readstate.readonly | Chat API | |
| classroom | ✅ | 10 classroom.* scopes | Classroom API | |
| drive | ✅ | drive | Drive API | |
| driveactivity | ✅ | drive.activity.readonly | Drive Activity API | Read-only audit |
| docs | ✅ | drive, documents | Docs API + Drive | Export/copy/create via Drive |
| slides | ✅ | drive, presentations | Slides API + Drive | Create/edit presentations |
| contacts | ✅ | contacts, contacts.other.readonly, directory.readonly | People API | Contacts + other + directory |
| tasks | ✅ | tasks | Tasks API | |
| sheets | ✅ | drive, spreadsheets | Sheets API + Drive | Export via Drive |
| people | ✅ | profile (OIDC) | People API | OIDC profile scope |
| forms | ✅ | forms.body, forms.responses.readonly | Forms API | |
| sites | ✅ | drive | Drive API | New Sites = Drive files |
| meet | ✅ | meetings.space.created, meetings.space.readonly, meetings.space.settings | Meet REST API | |
| appscript | ✅ | script.projects, script.deployments, script.processes | Apps Script API | |
| analytics | ✅ | analytics.readonly | Analytics Admin + Data API | GA4 reporting |
| searchconsole | ✅ | webmasters | Search Console API | Search Analytics + sitemaps |
| ads | ✅ | adwords | Google Ads API | OAuth scope only |
| youtube | ✅ | youtube.readonly | YouTube Data API v3 | Most read ops work with API key too |
| groups | ❌ | cloud-identity.groups.readonly | Cloud Identity API | Workspace only |
| keep | ❌ | keep | Keep API | Workspace only; service account |
| admin | ❌ | admin.directory.user, admin.directory.group, admin.directory.group.member | Admin SDK Directory API | Workspace only; domain-wide delegation |

## Recommended services for Flux Agency
```
gmail,calendar,drive,docs,slides,sheets,contacts,tasks,people,forms,meet,analytics,searchconsole,ads,youtube
```

## Read-only alternative
Append `--readonly` to use read-only scopes where available (still includes OIDC identity scopes).
