export class Room {
  #id;
  #name;
  #messages;

  constructor({ id, name, messages }) {
    this.#id = id;
    this.#name = name;
    this.#messages = messages.map(message => message.clone());
  }

  getId() {
    return this.#id
  }

  getName() {
    return this.#name;
  }

  getMessages() {
    return this.#messages.map(message => message.clone());
  }

  getMessage(id) {
    return this.#messages.find(message => message.getId() === id);
  }

  createMessage(message) {
    this.#messages.push(new Message({
      id: message.id,
      content: message.content,
      date: message.date,
      user: message.user
    }));
  }

  deleteMessage(id) {
    const deletedIndex = this.#messages.findIndex(message => message.getId() === id);
    if (deletedIndex) {
      this.#messages.splice(deletedIndex, 1);
    }
  }

  clone() {
    return new Room({
      id: this.#id,
      name: this.#name,
      messages: this.#messages
    });
  }
}

export class Message {
  #id;
  #content;
  #date;
  #user;

  constructor({ id, content, date, user }) {
    this.#id = id;
    this.#content = content;
    this.#date = date;
    this.#user = user;
  }

  getId() {
    return this.#id;
  }

  getContent() {
    return this.#content;
  }

  getDate() {
    return this.#date;
  }

  getUser() {
    return this.#user;
  }

  clone() {
    return new Message({
      id: this.#id,
      content: this.#content,
      date: this.#date,
      user: this.#user
    });
  }
}
