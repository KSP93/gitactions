# Trade Orders API - FastAPI, Docker & AWS EC2 Deployment

This project is a **scalable, containerized REST API** for trade orders, built using **FastAPI (Python)** and deployed on **AWS EC2** with **Docker**. It features **real-time updates via WebSockets**, a **CI/CD pipeline with GitHub Actions**, and a **PostgreSQL database** for data persistence.

---

## **🚀 Features**
✔️ **Trade Orders REST APIs** - Submit & retrieve trade orders  
✔️ **Swagger UI** - API documentation at `http://<EC2_PUBLIC_IP>:8080/docs`  
✔️ **WebSocket Real-Time Updates** - Clients receive instant order notifications  
✔️ **Containerized Deployment** - Docker ensures portability and consistency  
✔️ **CI/CD Automation** - GitHub Actions automates testing & deployment  

---

## **🛠 Tech Stack**
- **Backend:** FastAPI (Python)
- **Server:** Uvicorn (ASGI)
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose
- **Cloud Hosting:** AWS EC2 (Ubuntu)
- **Testing:** Pytest
- **WebSockets:** Real-time updates
- **CI/CD:** GitHub Actions

---

## **📌 API Endpoints**
| Method | Endpoint          | Description                        |
|--------|------------------|------------------------------------|
| **POST** | `/orders`         | Submit a new trade order          |
| **GET**  | `/Submitted_Orders` | Retrieve all submitted orders    |
| **WS**   | `/ws`            | WebSocket connection for updates |

### **Example API Request (Submit Order)**
```sh
curl -X POST "http://<EC2_PUBLIC_IP>:8080/orders?symbol=AAPL&price=150.0&quantity=10&order_type=buy"
```
### **Expected Response**
```json
{
  "id": "f5e0d20d-6f9d-4c1d-9f64-8c543f08a2b3",
  "symbol": "AAPL",
  "price": 150.0,
  "quantity": 10,
  "order_type": "buy"
}
```

---

## **🔧 Step 1: Develop APIs using FastAPI**
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Define an **Order Schema** using **Pydantic** for input validation.
3. Implement API endpoints:
   - `POST /orders`: Accepts trade order details.
   - `GET /Submitted_Orders`: Returns submitted orders.
4. Connect **PostgreSQL** for persistent data storage.
5. Implement **WebSockets** for real-time order updates.
6. Write **unit tests** using `pytest`.

---

## **🛡️ Step 2: Implement WebSockets for Real-Time Updates**
- Clients can connect to `/ws` to receive order updates.
- Server **broadcasts messages** when a new order is placed.
- Handles **disconnections** to prevent memory leaks.
- **Test WebSockets** using:
  ```sh
  pytest test_websocket.py
  ```

---

## **🐳 Step 3: Dockerize the Application**
### **1️⃣ Create a Dockerfile**
- Use a **Python base image**.
- Install dependencies from `requirements.txt`.
- Copy the FastAPI app into the container.
- Expose API on **port 8080**.

### **2️⃣ Build the Docker Image**
```sh
docker build -t trade-orders-app .
```

### **3️⃣ Run the Container**
```sh
docker run -p 8080:8080 trade-orders-app
```

### **4️⃣ Verify API in Docker**
- Use **Swagger UI**: `http://localhost:8080/docs`
- Test WebSockets using `pytest test_websocket.py`.

---

## **☁️ Step 4: Deploy API on AWS EC2**
### **1️⃣ Set Up an EC2 Instance**
- Launch an **Ubuntu instance**.
- Open **port 8080** in the security group.

### **2️⃣ Install Docker on EC2**
```sh
sudo apt update
sudo apt install -y docker.io
```

### **3️⃣ Deploy the Container**
```sh
docker-compose up -d
```

### **4️⃣ Verify API on EC2**
- Open `http://<EC2_PUBLIC_IP>:8080/docs` in a browser.
- Test the API with `curl`:
  ```sh
  curl -X GET "http://<EC2_PUBLIC_IP>:8080/Submitted_Orders"
  ```

---

## **🚀 Step 5: Automate Deployment with GitHub Actions**
### **1️⃣ Set Up GitHub Actions Workflow**
- Define a **CI/CD pipeline** in `.github/workflows/ci-cd.yml`.
- Trigger build & deploy **on every push** to `main`.

### **2️⃣ Run the CI/CD Pipeline**
- On every push:
  1. Runs **unit tests** with `pytest`
  2. Builds **Docker image**
  3. SSHs into EC2 & deploys the latest version

### **3️⃣ Deployment Script (via SSH)**
```sh
sudo docker stop trade-orders-app || true
sudo docker rm trade-orders-app || true
sudo docker run -d -p 8080:8080 --name trade-orders-app trade-orders-app
```

---

## **✅ Validations & Edge Cases**
### **Pydantic Input Validation**
- **Invalid Symbols** → Only **uppercase letters (A-Z)** allowed.
- **Negative Price/Quantity** → Must be **greater than zero**.
- **Invalid Order Type** → Must be **'buy' or 'sell'**.
- **Database Connection Failures** → **Handled gracefully**.

---

## **📜 Future Enhancements**
- Add **user authentication** for API security.
- Improve **database indexing** for faster queries.
- Implement **Kafka** for advanced real-time processing.

---

## **👨‍💻 Author**
🚀 **Shashi Preetham KOTTE**  
🌐 **GitHub:** [KSP93](https://github.com/KSP93)  
📧 **Email:** shashi.preetham2804@gmail.com  

---

## **🐟 License**
This project is **open-source** under the **MIT License**.

