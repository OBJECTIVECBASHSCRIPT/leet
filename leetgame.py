import random
import sys

class LeetGame:
    def __init__(self):
        self.level = 1
        self.flags = []
        self.lives = 2
        self.multiplier = 1
        self.running = True

        # 1337 perk related
        self.perk_1337 = False
        self.boost = 0
        self.error_free_graces = 0
        self.hits_per_life = 3  # default
        self.hits_left = 3      # tracks current hits left per life

    def start(self):
        print("leet: h4x0r edition")
        while self.running:
            # Offer to activate 1337 perk if available
            if not self.perk_1337 and len(self.flags) >= 25:
                choice = input("Activate 1337 perk for 25 flags? (y/n): ").strip().lower()
                if choice == 'y':
                    self.activate_1337_perk()
            self.play_level()

    def activate_1337_perk(self):
        if not self.perk_1337 and len(self.flags) >= 25:
            self.perk_1337 = True
            self.boost = 1
            self.error_free_graces = 3
            self.lives = 3
            self.hits_per_life = 7
            self.hits_left = 7
            self.flags = self.flags[100:]  # spend 100 flags
            print("🔥 1337 Perk Activated! 1 boost, 3 error-free graces, 3 lives, 7 hits per life.")
        elif self.perk_1337:
            print("1337 Perk already active.")
        else:
            print("Not enough flags for 1337 perk.")

    def play_level(self):
        pattern, answer, idx = self.generate_pattern()
        display = [str(val) if i != idx else "___" for i, val in enumerate(pattern)]

        print(f"\nLevel {self.level} | Lives: {int(self.lives)} | Flags: {len(self.flags)}")
        if self.perk_1337:
            print(f"1337 Perk ACTIVE | Boosts: {self.boost} | Graces: {self.error_free_graces} | Hits left: {self.hits_left}")
        print("Pattern:", ", ".join(display))

        user_input = input("Your answer (or 'q' to quit): ").strip()
        if user_input.lower() == 'q':
            self.quit_game("Game Quit")
            return

        try:
            if int(user_input) == answer:
                flag = self.generate_flag()
                self.flags.append(flag)
                print(f"✅ Correct! FLAG UNLOCKED: {flag}")
                self.level += 1
                if self.level > 255:
                    self.quit_game("MAX LEVEL REACHED")
            else:
                print(f"❌ Incorrect. The answer was {answer}.")
                # Perk logic: graces/hits/lives
                if self.perk_1337:
                    if self.error_free_graces > 0:
                        self.error_free_graces -= 1
                        print(f"Grace used! Graces left: {self.error_free_graces}")
                    else:
                        self.hits_left -= 1
                        print(f"Hit taken. Hits left this life: {self.hits_left}")
                        if self.hits_left <= 0:
                            self.lives -= 1
                            print(f"Life lost! Lives left: {self.lives}")
                            if self.lives > 0:
                                self.hits_left = self.hits_per_life
                        if self.lives <= 0:
                            self.quit_game("Game Over")
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.quit_game("Game Over")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

    def generate_pattern(self):
        is_geo = self.level % 2 == 0
        start = random.randint(2, 6)
        step = random.randint(2, 5) + self.level // 10
        length = min(6 + self.level // 10, 10)
        seq = [start]
        for _ in range(1, length):
            seq.append(seq[-1] * step if is_geo else seq[-1] + step)
        idx = random.randint(1, length - 2)
        return seq, seq[idx], idx

    def generate_flag(self):
        suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
        return f"FLAG-L{self.level}-{suffix}"

    def quit_game(self, message):
        print(f"\n{message}")
        print(f"Total Flags: {len(self.flags)}")
        print(f"Total Points: {len(self.flags) * 10 * self.multiplier}")
        self.running = False

if __name__ == "__main__":
    game = LeetGame()
    game.start()
