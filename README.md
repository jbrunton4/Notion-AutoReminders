# Notion-AutoReminders
Sends email reminders about notion pages routinely after some date property.

The original inspiration for this project was to make a service to provide
automated reminders to review study notes after they were created, based on
Ebbinghaus' Curve of Forgetting. 

## How to use
There are a few pieces of information that you need to give the app in order for it to work.

First, open the file named `config.json` in your favourite text editor.
Inside this file, you need to set the following values:

* database_id
* notion_token
* property_name
* email_addr
* email_password
* your_email
* reminder_intervals

## How To Get Config Values
### database_id
The database ID is the unique identifier for your table, list, or other database.
You can find this by first getting the link to your notion page, which should
look something like this:

`notion.so/My-Page-Name-a1b23c4de5f67890g12hh3456ij7kl89`
<br>or<br>
`notion.so/a1b23c4d-e5f6-7890-g12h-h3456ij7kl89?v=a1b2c3`

Your database ID is the long alphanumeric code here:
<br>notion.so/My-Page-Name`a1b23c4de5f67890g12hh3456ij7kl89`
<br>notion.so`a1b23c4d-e5f6-7890-g12h-h3456ij7kl89`?v=a1b2c3

Paste this code: `{"database_id": "Here, inside the quotation marks"}`.

### notion_token
To create a notion token, first open your notion app, then go to:
`Settings & Members > Integrations > Develop your own integrations > Create New Integration`.

Set the Integration type to "Internal integration", and make sure the "Read content" checkbox is enabled.

Finally, set User Capabilities to "Read user information including email addresses".

Now, your token should be at the top of the page. Click "show" and copy it into `config.json`.

[Create an integration here.](https://www.notion.so/my-integrations/)

### date_property_name
The name of the date property on which the page was first studied.
This is case-sensitive, so remember to use capital letters where appropriate.

### email_addr and email_password
These are an email address and password for a gmail account.

For the app to work, you will need to enable "Less Secure Apps" on your
Google account - since this required 2-factor authentication to be turned off,
you shouldn't use your personal email account.

[Enable less secure apps here.](https://myaccount.google.com/lesssecureapps)

### your_email
It's pretty much what it says on the tin: Your email. Reminders will be sent to this address.

### reminder_intervals
These are the number of days after the date listed in the database that you
would like to be reminded on. For example, if you want to be reminded
1, 2, and 7 days after, you would set it to `{"reminder_intervals":[1, 2, 7]}`.

## How to keep it running
In order for your reminders to be sent, the app needs to be constantly running.
You can host the script 24/7 for free using Heroku, or simply run the EXE on your computer.
