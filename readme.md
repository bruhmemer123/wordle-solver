# 🤖 Automated Wordle Solver (Information Theory)

A fully automated Python bot that plays the official New York Times Wordle game using **Shannon Entropy** and **Selenium WebDriver**. The bot dynamically reads the board state, calculates the mathematically optimal guess to maximize information gain, and solves the puzzle completely on its own.

## 🚀 Features
* **Information Theory Backend:** Calculates Shannon Entropy for every possible word loop to minimize the remaining solution space.
* **Live Browser Automation:** Uses Selenium WebDriver to handle NYT cookie banners, click through splash screens, and execute human-like typing intervals.
* **Dynamic HTML Scraping:** Targets dynamic web component layouts (`aria-labels` and `data-state` attributes) to accurately read tile colors in real-time.

## 📊 How the Math Works
Instead of guessing randomly, the bot scores every available word by how evenly it splits the remaining word pool across the 243 possible Wordle color combinations. It prioritizes choices that guarantee the largest reduction in uncertainty, optimizing the formula:

$$H(X) = -\sum P(x_i) \log_2 P(x_i)$$

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/wordle-solver.git](https://github.com/YOUR_USERNAME/wordle-solver.git)
   cd wordle-solver