/* Singleton for managing user session. */
export class SessionManager {
  static #instance;
  #rooms = [];
  #sessionToken;
  #wsSessionToken;
  #userId;
  #userRole;

  constructor() {
    if (SessionManager.#instance) {
      return SessionManager.#instance;
    }
    SessionManager.#instance = this;
  }

  getRooms() {
    return this.#rooms.map(room => room.clone());
  }

  getRoom(roomId) {
    return this.#rooms.find(room => room.getId() === roomId);
  }

  getMessage(roomId, messageId) {
    return this.#rooms.find(room => room.getId() === roomId)?.getMessage(messageId);
  }

  createMessage(roomId, message) {
    this.#rooms.find(room => room.getId() === roomId)?.createMessage(message);
  }

  deleteMessage(roomId, messageId) {
    this.#rooms.find(room => room.getId() === roomId)?.deleteMessage(messageId);
  }
}
