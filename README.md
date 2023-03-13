# Emo-Face

## How to start the service
```
git clone git@github.com:icytailovo/Emo-Face.git
```
We need to have two terminals, one for the client side, and the other for the server side.

### Client
```
cd client
npm install
npm start
```

### Server
1. Open a separate terminal
```
cd server/src
pip install openai
```
2. Either ask project admin or get an OpenAI API key through [this guide](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key).
3. In the `pic_edit.py` file, set the OpenAI API key
4. Start the server
```
python server.py
```

## Other Settings
For any photos that you want to add emoji on, put it into the `/images` folder relative to the project root.