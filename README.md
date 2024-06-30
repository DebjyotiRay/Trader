# Trader



## [Video presentation](https://youtu.be/c6nTzrCUwo8)

PITCH DECK:
![image](https://github.com/DebjyotiRay/Trader/assets/33850567/02d9b972-8488-487c-b819-1c1a46adde63)

![image](https://github.com/DebjyotiRay/Trader/assets/33850567/51316875-d633-44cf-9b94-4c0ff08e9e12)
![image](https://github.com/DebjyotiRay/Trader/assets/33850567/b8fd9379-74c4-48d2-881f-c422adbd190d)


# DRL Trader

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Walkthrough](#project-walkthrough)
  - [Data Gathering and Preprocessing](#data-gathering-and-preprocessing)
  - [DRL Model Execution](#drl-model-execution)
  - [Action to Trade Translation](#action-to-trade-translation)
  - [Portfolio Value Update](#portfolio-value-update)
  - [Reward Calculation and Learning](#reward-calculation-and-learning)
  - [Continual Iteration](#continual-iteration)
  - [Real-World Transition](#real-world-transition)
- [Flask API Implementation](#flask-api-implementation)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Introduction
**DRL Trader** is an intelligent system designed to revolutionize multi-stock portfolio trading. Leveraging the power of Deep Reinforcement Learning (DRL), it generates precise trading signals based on comprehensive analysis of technical indicators and historical market data. The bot's main objective is to optimize investment strategies by making informed decisions, thereby maximizing returns and minimizing risks in the complex stock market.

## Features
- **Deep Reinforcement Learning (DRL)**: Uses advanced DRL algorithms to generate trading signals.
- **Technical Indicators**: Analyzes key technical indicators such as MACD, RSI, CCI, and ADX.
- **Dynamic Portfolio Management**: Continuously updates and optimizes portfolio value.
- **Flask API**: Seamless execution and interaction with the trading bot through a user-friendly API.

## Project Walkthrough

### Data Gathering and Preprocessing
At each time step, market data, including open-high-low-close prices of Dow 30 stocks, are collected. Essential technical indicators such as MACD, RSI, CCI, and ADX are calculated, forming the "states" for our DRL model.

### DRL Model Execution
Our trained DRL model processes the states and generates a list of trading actions, each representing a specific stock. These actions, ranging from strong buy to strong sell, are meticulously determined to maximize gains.

### Action to Trade Translation
The trading actions are translated into tangible trading steps by calculating the number of shares to trade for each stock. Our predefined parameter, `h_max`, controls the maximum amount of shares to trade, ensuring optimal trading decisions.

### Portfolio Value Update
As the trading day progresses, our portfolio value is updated using the balance and dollar amount of stocks held. This dynamic updating reflects the ever-changing positions and performance.

### Reward Calculation and Learning
The DRL model's performance is evaluated by calculating the step reward (r) – the change in portfolio value from one time step to the next. This reward reinforces learning, enabling the model to adapt and optimize its strategies.

### Continual Iteration
This iterative process continues, allowing the DRL Trader to learn and evolve in response to varying market dynamics. The model's ability to swiftly capture returns amidst volatility is refined, leading to improved trading decisions.

### Real-World Transition
As we move towards real-world applications, the DRL Trader undergoes seamless integration, ensuring its performance aligns with real-time market conditions and adheres to the learned strategies.

## Flask API Implementation
To facilitate seamless execution and interaction with the "DRL Trader," we implemented a Flask API. This API serves as a bridge between the user and the bot. Upon user request, the API triggers the DRL model's execution, generating trading signals for each stock in the portfolio. These signals, reflecting strong buy or sell recommendations, offer a clear strategy for each stock.

## Ongoing Experiments and MT5 Integration
Our team is continuously thriving and making changes in the `experiments` subfolder. We are actively working on setting up the MT5 connection to our broker to execute all of our DRL decisions simultaneously and seamlessly. This integration aims to enhance the real-world applicability and efficiency of the DRL Trader by automating trade execution.

## Installation
To install and run the DRL Trader, follow these steps:

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/drl-trader.git
    cd drl-trader
    ```

2. **Create a Virtual Environment**
    ```sh
    python3 -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
    - Create a `.env` file in the root directory of the project and add necessary environment variables.

5. **Run the Flask API**
    ```sh
    flask run
    ```

## Usage
Once the Flask API is running, you can interact with the DRL Trader through API endpoints.

- **Trigger Trading Signal Generation**
    ```sh
    curl -X POST http://localhost:5000/api/trade -d '{"stocks": ["AAPL", "MSFT", "GOOGL"]}'
    ```

- **Check Portfolio Value**
    ```sh
    curl -X GET http://localhost:5000/api/portfolio
    ```

## Contributing
We welcome contributions to enhance the DRL Trader. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

Please ensure your code adheres to our coding standards and includes relevant tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact Information
For questions or support, please contact:

- **Email**: sapphireinc2100@gmail.com
- **GitHub Issues**: [https://github.com/DebjyotiRay/Trader/issues](https://github.com/DebjyotiRay/Trader/issues)

---

Feel free to adjust any sections or add more details as necessary for your project.
