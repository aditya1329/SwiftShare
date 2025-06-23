# ⚡ SwiftShare – High-Speed Offline File Transfer System

**SwiftShare** is a high-performance, multi-threaded file transfer system that enables users to send and receive large files across devices **without using the internet**. It utilizes sockets and threading to facilitate fast, peer-to-peer (P2P) offline file sharing.

---

## 🚀 Features

- 📁 Upload and download large files between devices
- 🔄 Offline sharing — no need for cloud (e.g., Google Drive, Dropbox)
- ⚡ Multi-threaded architecture for faster file transfers
- 🔒 Local network communication using sockets
- 🖥️ Simple CLI-based interface (can be extended to GUI)


---

## 🔧 Technologies Used

- **Language**: Python
- **Networking**: Sockets
- **Concurrency**: Multithreading
- **OS Module**: For file operations and path handling

---

## 🧠 How It Works

1. **Sender** selects a file to share.
2. **Receiver** runs the receiver script and listens on a specified port.
3. SwiftShare establishes a socket connection on the same network (LAN).
4. The file is transferred in chunks using **multi-threading** to improve performance.
5. File is reconstructed and saved at the receiver’s end.

---

