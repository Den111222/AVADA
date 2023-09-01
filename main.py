#Russian
"""
Данное ТЗ на позицию junior python dev.
Данное ТЗ заняло у меня 4 полных рабочих дня или 32 часа.

Требование к коду : использование ООП  (обьектно -ориентированное программирование ) 
Готовый результат :  предоставить  ссылку на GitHub репозиторий  
Интерфейс: ввод и вывод в консоли ( input,print .без графического интерфейса )
Библиотеки которые можно использовать:  numpy, collections, json, logging, itertools, Enum

Игровая Карта 👇🏻 


Вам нужно написать код, который позволит героям пройти по лабиринту.
То есть, вам нужно придумать реализацию системы управления и проверки решений. Управление: Вверх, вниз, влево, вправо
через инпут или при нажатии клавиши, как хотите. + Возможность бить мечом и поднимать ключ.
Передвижение тратит действие героя. Если наступить на клетку с зеленым сердцем то при этом восстанавливается всё 
здоровье, сердце не исчезает.

Герои обладают 5 единицами Жизни, возможностью бить всех героев в той же клетке мечом(тратит действие), могут поднять 
ключ (при этом он исчезает из клетки, тратит действие), лечиться самостоятельно (3 заряда по 1 Жизни, тратит действие)

УСЛОВИЯ :

При старте игры предлагаем выбрать число героев. Затем предлагаем каждому игроку ввести имя своего Героя.
Затем Герои начинают по очереди ходить, их действия и результаты действий логируются с помощью logging и выводятся в 
консоль.
Если Герой выбрал направление с клеткой, то выводим в консоль результат перехода (получил ли персонаж урон от огня, 
есть ли в новой клетке другие герои, получил ли герой лечение, есть ли в клетке ключ) и даем следующий ход другому 
герою.
Если Герой пошел в сторону стены - пишем, что герой ударился о стену, герой теряет 1 очко жизни.
Герой не может пропустить ход.
Если Герой вернулся туда откуда пришел на предыдущем ходу - выводим Герой струсил и убежал, Герой выводится из игры. 
При переходе на оранжевые клетки последний ход не меняем (чтобы герой мог зайти на оранжевую клетку и вернуться, но не 
смог после этого пойти назад)
Если Герой закончил ход с 0 очков жизней (т.е. очки упали на его ход) - выводим Герой погиб, Герой выводится из игры.
При гибели или побеге если у Героя был ключ, ключ выпадает в 
Если Герой начал ход с 0 очков жизней (его убил другой герой мечом на свой ход) - выводим Герой погиб, Герой выводится 
из игры.
Если Герой с ключом дошёл до Голема(клетка финиш) - игра заканчивается и выводим что герой с этим именем победил.
Если Герой без ключа дошёл до Голема(клетка финиш) - Герой погибает (его убивает голем), герой, выводится из игры.
Перед началом каждого нового раунда ходов на четырёх случайных белых клетках загорается огонь. Если шагнуть на клетку 
с огнем - герой теряет одну жизнь. В начале каждого раунда сообщаются координаты клеток с огнём 

ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ :

Реализовать систему сохранений в JSON. 
В любой момент мы можем сохранить прогресс игры, местоположение и статусы всех героев. При запуске новой игры 
происходит проверка на наличие сохранения. Если есть сохранение - предлагаем загрузить его. При отказе удаляем 
сохранение и начинаем новую игру с нуля, предлагая выбрать число игроков.

"""
#English
"""
This TOR (terms of reference) is for a junior python dev position.
This TOR took me 4 full working days or 32 hours.

Code requirement : use OOP (Object Oriented Programming). 
Finished result : provide a link to the GitHub repository  
Interface : console input and output ( input,print .no GUI )
Libraries that can be used: numpy, collections, json, logging, itertools, Enum

Game Map 👇🏻 


You need to write code that will allow the heroes to walk through a maze.
That is, you need to come up with an implementation of a control and decision checking system. Controls: Up, down, 
left, right.
Via input or keypress, whatever you want. + Ability to hit with sword and lift key.
Moving around spends the hero's action. Stepping on a square with a green heart restores all of your 
health, the heart does not disappear.

Heroes have 5 units of Life, the ability to hit all heroes in the same square with a sword (spends an action), can 
raise a key (it disappears). 
key (it disappears from the cage, spends an action), heal themselves (3 charges of 1 Life, spends an action).

CONDITIONS :

At the start of the game, we suggest choosing the number of heroes. Then we suggest each player to enter the name 
of his Hero.
Then the Heroes start taking turns, their actions and results are logged with logging and output to the 
console.
If the Hero has chosen a direction with a cell, then output to the console the result of the transition (whether 
the character received damage from fire, 
whether there are other heroes in the new cage, whether the hero received treatment, whether there is a key in the 
cage) and give the next move to another 
hero.
If the hero went towards the wall - write that the hero hit the wall, the hero loses 1 life point.
Hero can not miss a move.
If the hero returned to where he came from on the previous turn - withdraw Hero chickened out and ran away, the hero 
is withdrawn from the game. 
When moving to orange squares the last move is not changed (so that the hero can go to the orange square and return, 
but could not after that go back). 
be able to go back after that)
If the Hero finished his turn with 0 life points (i.e. points fell on his turn) - withdraw Hero is killed, Hero is 
withdrawn from the game.
At death or escape if the Hero had a key, the key falls in 
If the Hero started the turn with 0 life points (he was killed by another hero with a sword on his turn) - take out 
the Hero died, the Hero is removed from the game 
out of the game.
If the Hero with the key reached the Golem (cell finish) - the game ends and deduce that the hero with this name won.
If the Hero without the key reached the Golem (cell finish) - the Hero dies (he is killed by the Golem), the hero is 
taken out of the game.
Before the start of each new round of moves, a fire is lit on four random white squares. If you step on a square 
with fire, the hero loses one life. At the beginning of each round, the coordinates of the squares with fire are 
announced 

ADDITIONAL TASK :

Realize the system of saves in JSON. 
At any moment we can save game progress, location and statuses of all heroes. When starting a new game 
we check if there is a save. If there is a save - we offer to load it. In case of refusal we delete 
save and start a new game from scratch, offering to choose the number of players.
"""
from src.game_start import start_game

if __name__ == '__main__':
    start_game()