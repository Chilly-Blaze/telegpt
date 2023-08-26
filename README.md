# telegpt
Telegram Bot + ChatGPT3.5 with customized prompt

## Installation
Ensure that the **>=python3.10** environment exists

1. Download ZIP and Extract
2. Move to the project directory(`cd [download dir]/telegpt`)
3. `pip install -r requirements.txt`
4. Modify the `tele_api` and `chat_api` in `config.json` to your own
   - `tele_key` is in [BotFather](https://t.me/BotFather) -> `/newbot` -> your_bot -> API token
   - `chat_key` is in [OpenAI API](https://platform.openai.com/account/api-keys)
   - `entry_key` is a password you like
   - `master_key` is your telegram user id in [userinfobot](https://t.me/userinfobot)
5. `python3 -u main.py` or `python3 -u main.py 1>info.log 2>error.log` to write log to file

## Usage

### All users' permissions
- `/start [entry_key]` Start to conversation.
- `/reset` Reset current prompt. It will delete history conversation.
- `/show` Show a role's prompt.
- `/now` Show current prompt.
- `/regenerate` Regenerate last reply.
- `[TEXT]` Chat with ChatGPT.
### Only master's permissions
- `/new` Create a new role.
- `/edit` Choose a role and edit its prompt.
- `/switch` Switch another role.
- `/del` Delete a role

Enjoy!
