<script>
  let level = 1, lives, difficulty, multiplier, sequence = [], correctAnswer, missingIndex;
  let flags = JSON.parse(localStorage.getItem("flags")) || [];
  let timerInterval = null;
  let timeLeft = 10;
  let aiTimeout = null;
  let aiInterval = null;
  let winner = null;
  let mode = "P1";

  function setOpponentMode(selectedMode) {
    mode = selectedMode;
    document.getElementById("difficultyOptions").classList.remove("hidden");
  }

  function startGame(diff, lifeCount, multi) {
    difficulty = diff;
    lives = lifeCount;
    multiplier = multi;
    level = 1;
    flags = [];
    localStorage.setItem("flags", JSON.stringify(flags));
    document.getElementById("startScreen").classList.add("hidden");
    document.getElementById("gameScreen").classList.remove("hidden");
    document.getElementById("difficultyDisplay").textContent = difficulty;

    document.getElementById("inputP1").classList.add("hidden");
    document.getElementById("inputP2").classList.add("hidden");
    document.getElementById("inputAI").classList.add("hidden");
    if (mode === 'P1') document.getElementById("inputP1").classList.remove("hidden");
    if (mode === 'P2') document.getElementById("inputP2").classList.remove("hidden");
    if (mode === 'AI') document.getElementById("inputAI").classList.remove("hidden");

    updateUI();
    getPattern();
  }

  function startClock() {
    const clockEl = document.getElementById("clock");
    setInterval(() => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      const ss = String(now.getSeconds()).padStart(2, '0');
      clockEl.textContent = `🕒 ${hh}:${mm}:${ss}`;
    }, 1000);
  }

  function updateUI() {
    document.getElementById("levelDisplay").textContent = level;
    document.getElementById("livesDisplay").textContent = lives === Infinity ? '∞' : lives;
    document.getElementById("flagsDisplay").textContent = flags.length;
  }

  function getPattern() {
    generatePatternFallback();
  }

  function generatePatternFallback() {
    const isFibo = level % 2 === 0;
    const length = 6;
    sequence = [];
    if (isFibo) {
      let a = Math.floor(Math.random() * 3) + 1, b = a;
      sequence.push(a, b);
      for (let i = 2; i < length; i++) sequence.push(sequence[i - 1] + sequence[i - 2]);
    } else {
      let start = Math.floor(Math.random() * 10) + 1, step = Math.floor(Math.random() * 5) + 2;
      for (let i = 0; i < length; i++) sequence.push(start + i * step);
    }
    missingIndex = Math.floor(Math.random() * (length - 2)) + 1;
    correctAnswer = sequence[missingIndex];
    sequence[missingIndex] = null;
    renderPattern();
  }

  function renderPattern() {
    const display = sequence.map((val, idx) => idx === missingIndex ? '?' : val).join(", ");
    document.getElementById("patternDisplay").innerHTML = display;
    document.getElementById("result").textContent = "";
    document.getElementById("flagDisplay").textContent = "";
    if (mode === 'AI') startAIChallenge();
  }

  function startAIChallenge() {
    let aiProgress = 0;
    const aiSpeed = getAISpeed();
    const progressDiv = document.getElementById("aiProgress");
    aiInterval = setInterval(() => {
      aiProgress += 10;
      progressDiv.textContent = `💻 AI Progress: ${aiProgress}%`;
    }, aiSpeed / 10);
    aiTimeout = setTimeout(() => {
      clearInterval(aiInterval);
      aiWins();
    }, aiSpeed);
  }

  function getAISpeed() {
    switch (difficulty) {
      case "Peaceful": return 999999;
      case "Easy": return 8000;
      case "Medium": return 6000;
      case "Hard": return 4000;
      case "Veteran": return 3000;
      default: return 5000;
    }
  }

  function aiWins() {
    alert("💻 AI solved the pattern before you!\nGAME OVER.");
    endGame("AI won the round.");
  }

  function generateFlag() {
    const suffix = Math.random().toString(36).substring(2, 6).toUpperCase();
    const flag = `FLAG{LEVEL_${level}_${suffix}}`;
    flags.push(flag);
    localStorage.setItem("flags", JSON.stringify(flags));
    return flag;
  }

  function checkAnswer(player) {
    if (winner) return;
    const inputId = player === 1 ? 'userInputP1' : 'userInputP2';
    const userVal = parseInt(document.getElementById(inputId).value);
    const result = document.getElementById("result");
    const flag = document.getElementById("flagDisplay");

    if (userVal === correctAnswer) {
      winner = `Player ${player}`;
      result.textContent = `✅ ${winner} Correct!`;
      result.style.color = "#00FF00";
      const newFlag = generateFlag();
      flag.textContent = `🎉 FLAG UNLOCKED: ${newFlag}`;
      level++;
      updateUI();
      setTimeout(() => {
        winner = null;
        getPattern();
      }, 3000);
    } else {
      result.textContent = `❌ Player ${player} Incorrect.`;
      result.style.color = "red";
    }
  }

  function quitGame() {
    clearInterval(timerInterval);
    clearTimeout(aiTimeout);
    clearInterval(aiInterval);
    endGame("⏹ Game Quit");
  }

  function endGame(message) {
    clearInterval(timerInterval);
    clearTimeout(aiTimeout);
    clearInterval(aiInterval);
    const totalPoints = flags.length * 10 * multiplier;
    alert(`${message}\nFlags: ${flags.length}\nPoints: ${totalPoints}`);
    document.getElementById("gameScreen").classList.add("hidden");
    document.getElementById("startScreen").classList.remove("hidden");
    document.getElementById("aiProgress").textContent = "";
  }

  startClock();
</script>
