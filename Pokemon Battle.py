import tkinter as tk
from tkinter import ttk, scrolledtext
import random

class Pokemon:
    def __init__(self, name, hp, element_type, basic_attack_damage, elemental_skill_damage, burst_skill_damage):
        self.name = name
        self._max_hp = hp
        self.hp = hp
        self.element_type = element_type
        self.basic_attack_damage = basic_attack_damage
        self.elemental_skill_damage = elemental_skill_damage
        self.burst_skill_damage = burst_skill_damage

    def calculate_damage(self, damage, target_element_type):
        type_weakness = {
            "Fighting": ["Normal"],
            "Water": ["Fire"],
            "Ground": ["Fire", "Electric", "Rock"],
            "Rock": ["Fire", "Ice", "Fighting", "Bug"],
            "Electric": ["Water"],
            "Fire": ["Grass", "Bug", "Ice"],
            "Flying": ["Fighting", "Bug", "Grass"],
            "Psychic": ["Fighting", "Bug", "Ghost"],
            "Poison": ["Grass", "Fairy"],
            "Bug": ["Grass", "Psychic", "Dark"],
            "Ghost": ["Ghost", "Dark"],
            "Steel": ["Ice", "Rock", "Fairy"],
            "Ice": ["Fire", "Fighting", "Rock", "Steel"],
            "Dark": ["Psychic"],
            "Fairy": ["Fighting", "Dragon"],
            "Dragon": ["Dragon", "Ice", "Fairy"],
            "Grass": ["Water", "Rock", "Ground"]
        }

        if target_element_type in type_weakness[self.element_type]:
            return damage * 2, "IT'S Super Effective"
        else:
            return damage, ""
        
    @property
    def max_hp(self):
        return self._max_hp
        
    def basic_attack(self, target):
        damage, effectiveness = self.calculate_damage(self.basic_attack_damage, target.element_type)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage, effectiveness

    def elemental_skill(self, target):
        damage, effectiveness = self.calculate_damage(self.elemental_skill_damage, target.element_type)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage, effectiveness

    def burst_skill(self, target):
        damage, effectiveness = self.calculate_damage(self.burst_skill_damage, target.element_type)
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage, effectiveness
    
    def heal_potion(self, amount):
        self.hp += amount
        if self.hp > self._max_hp:
            self.hp = self._max_hp
        
class PokemonBattleApp:
    def __init__(self, master):
        self.victory_status = False
        self.master = master
        self.master.title("Pokemon Battle")
        self.master.geometry("1000x500")
        self.master.attributes('-toolwindow', True)

        self.pokemon_data = {
            "Pikachu": Pokemon("Pikachu", 450, "Electric", 5, 25, 35),
            "Charmander": Pokemon("Charmander", 670, "Fire", 5, 20, 30),
            "Bulbasaur": Pokemon("Bulbasaur", 500, "Grass", 6, 22, 32),
            "Squirtle": Pokemon("Squirtle", 400, "Water", 3, 21, 30),
            "Caterpie": Pokemon("Caterpie", 380, "Bug", 7, 19, 33),
            "Ekans": Pokemon("Ekans", 500, "Poison", 1, 10, 50),
            "Sandshrew": Pokemon("Sandshrew", 500, "Ground", 1, 10, 40),
            "Clefairy": Pokemon("Clefairy", 500, "Fairy", 1, 10, 62),
            "Mankey": Pokemon("Mankey", 500, "Fighting", 1, 10, 40),
            "Abra": Pokemon("Abra", 500, "Psychic", 1, 10, 43),
            "Gastly": Pokemon("Gastly", 500, "Ghost", 1, 10, 30),
            "Geodude": Pokemon("Geodude", 500, "Rock", 1, 10, 30),
            "Dratini": Pokemon("Dratini", 500, "Dragon", 1, 10, 28),
            "Honedge": Pokemon("Honedge", 500, "Steel", 1, 10, 21),
            "Inkay": Pokemon("Inkay", 500, "Dark", 1, 10, 78)

        }


        self.user_pokemon = self.choose_random_pokemon()
        self.enemy_pokemon = self.choose_random_pokemon_for_enemy(self.user_pokemon)

        self.create_widgets()

    def choose_random_pokemon(self):
        # Pilih secara acak satu Pokemon dari dictionary
        chosen_pokemon = random.choice(list(self.pokemon_data.values()))
        return chosen_pokemon

    def choose_random_pokemon_for_enemy(self, player_pokemon):
        # Pilih secara acak Pokemon untuk musuh
        while True:
            enemy_pokemon = self.choose_random_pokemon()
            if enemy_pokemon != player_pokemon:
                return enemy_pokemon

    def create_widgets(self):
        enemy_frame = tk.Frame(self.master)
        enemy_frame.pack(side=tk.LEFT, padx=100)

        self.enemy_name_label = tk.Label(enemy_frame, text=f"{self.enemy_pokemon.name}")
        self.enemy_name_label.pack()

        self.enemy_hp_bar = ttk.Progressbar(enemy_frame, orient='horizontal', length=200, mode='determinate')
        self.enemy_hp_bar.pack()

        self.enemy_hp_label = tk.Label(enemy_frame, text=f"HP: {self.enemy_pokemon.hp}")
        self.enemy_hp_label.pack()

        vs_label = tk.Label(enemy_frame, text="\n\n\n\nVS\n\n\n\n")
        vs_label.pack(side=tk.TOP, padx=10)

        user_frame = tk.Frame(enemy_frame)
        user_frame.pack(side=tk.TOP, padx=10)

        self.user_name_label = tk.Label(user_frame, text=f"{self.user_pokemon.name}")
        self.user_name_label.pack()

        self.user_hp_bar = ttk.Progressbar(user_frame, orient='horizontal', length=200, mode='determinate')
        self.user_hp_bar.pack()

        self.user_hp_label = tk.Label(user_frame, text=f"HP: {self.user_pokemon.hp}")
        self.user_hp_label.pack()

        self.attack_button = tk.Button(user_frame, text="Basic Attack", command=self.user_attack)
        self.attack_button.pack()

        self.elemental_button = tk.Button(user_frame, text="Elemental Skill", command=self.user_elemental_skill)
        self.elemental_button.pack()

        self.burst_button = tk.Button(user_frame, text="Burst Skill", command=self.user_burst_skill)
        self.burst_button.pack()

        self.heal_button = tk.Button(user_frame, text="Heal Potion", command=self.user_heal_potion)
        self.heal_button.pack()

        self.log_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=70)
        self.log_text.pack(side=tk.RIGHT, padx=10)

    def user_attack(self):
        damage, effectiveness = self.user_pokemon.basic_attack(self.enemy_pokemon)
        self.update_display(f"{self.user_pokemon.name} uses Basic Attack and deals {damage} damage. {effectiveness}")
        self.enemy_attack()

    def user_elemental_skill(self):
        damage, effectiveness = self.user_pokemon.elemental_skill(self.enemy_pokemon)
        self.update_display(f"{self.user_pokemon.name} uses Elemental Skill and deals {damage} damage. {effectiveness}")
        self.enemy_attack()

    def user_burst_skill(self):
        damage, effectiveness = self.user_pokemon.burst_skill(self.enemy_pokemon)
        self.update_display(f"{self.user_pokemon.name} uses Burst Skill and deals {damage} damage. {effectiveness}")
        self.enemy_attack()

    def user_heal_potion(self):
        heal_amount = 100
        self.user_pokemon.heal_potion(heal_amount)
        self.update_display(f"{self.user_pokemon.name} uses Heal Potion and heals {heal_amount} HP.")
        self.enemy_attack()

    def enemy_attack(self):
        if random.random() < 0.95:
            skill = random.choice([self.enemy_pokemon.basic_attack, self.enemy_pokemon.elemental_skill, self.enemy_pokemon.burst_skill])
            damage, effectiveness = skill(self.user_pokemon)
            self.update_display(f"Enemy {self.enemy_pokemon.name} uses {skill.__name__} and deals {damage} damage. {effectiveness}")
        else:
            heal_amount = 100
            self.enemy_pokemon.heal_potion(heal_amount)
            self.update_display(f"Enemy {self.enemy_pokemon.name} uses Heal Potion and heals {heal_amount} HP.")

    def update_display(self, log_entry):
        if self.user_pokemon.hp <= 0:
            self.show_result(f"You lose! Game over!\n{self.user_pokemon.name} KO'd, {self.enemy_pokemon.name} WINS")
            self.disable_buttons()
        elif self.enemy_pokemon.hp <= 0 and not self.victory_status:
            self.show_result(f"Congratulations! You win!\n{self.enemy_pokemon.name} KO'd, {self.user_pokemon.name} WINS")
            self.disable_buttons()
            self.victory_status = True

        self.enemy_name_label.config(text=f"{self.enemy_pokemon.name}")
        self.enemy_hp_label.config(text=f"HP: {self.enemy_pokemon.hp}")
        
        self.enemy_hp_bar["maximum"] = self.enemy_pokemon.max_hp
        self.enemy_hp_bar["value"] = self.enemy_pokemon.hp

        self.user_name_label.config(text=f"{self.user_pokemon.name}")
        self.user_hp_label.config(text=f"HP: {self.user_pokemon.hp}")
        
        self.user_hp_bar["maximum"] = self.user_pokemon.max_hp
        self.user_hp_bar["value"] = self.user_pokemon.hp

        self.log_text.insert(tk.END, log_entry + "\n")
        self.log_text.yview(tk.END)

    def show_result(self, result_text):
        result_label = tk.Label(self.master, text=result_text)
        result_label.pack(side=tk.BOTTOM)

    def disable_buttons(self):
        self.attack_button.config(state=tk.DISABLED)
        self.elemental_button.config(state=tk.DISABLED)
        self.burst_button.config(state=tk.DISABLED)
        self.heal_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonBattleApp(root)
    root.mainloop()