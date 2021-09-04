import vk_api
import json
from pprint import pprint
import re
from copy import deepcopy
from vk_api.longpoll import  VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard
vk_session = vk_api.VkApi(token="50e232192af3719b7e80b341b479c2665be8a8d012de1882101dceb003fa86eb28cfb80c10b090a2644db")
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)
vk_user_session = vk_api.VkApi(token="db176e08c29211bc00d3d72ee21b96cca5ae7ee2ea268312a8dcf3a959e0883f0416bf9ad7ca2969df270")

class User:
    def __init__(self):
        self.id=''
        self.name=''
        self.side=''
        self.lvl=1
        self.accLvl=0
        self.State='null'

Users=[]
def fillUsersArray():
    objects = vk_user_session.method('board.getComments', {'group_id': 118649434, 'topic_id': 47958603})
    objNorma=str(objects)
    objArr=objNorma[objNorma.find("{[")+2:].split("}, {")
    for i in range(len(objArr)):
        if(i==0):
            i+=1
            continue
        else:
            cuttedName=objArr[i][objArr[i].find("ажа :")+5:]
            cuttedPastNameRaw=re.search("2",cuttedName)

            cutteCharName=cuttedName[:cuttedPastNameRaw.start()-4]

            cuttedSide=objArr[i][objArr[i].find("торона :")+8:]

            cuttedCharSide=cuttedSide[:cuttedSide.find('\'')]

            cuttedId = objArr[i][objArr[i].find("2) Код персонажа:") + 17:]
            cuttedIdRaw=re.search("3\)",cuttedId)

            cuttedCharId=cuttedId[:cuttedIdRaw.start()-3]

            cuttedLvl= objArr[i][objArr[i].find("Игровой уровень:") + 16:]
            cuttedLvlRaw=re.search("\|",cuttedLvl)

            cuttedCharLvl=cuttedLvl[1:cuttedLvlRaw.start()-1]

            cuttedAccLvl = objArr[i][objArr[i].find("Уровень аккаунта :") + 18:]
            cuttedAccLvlRaw = re.search("6\)", cuttedAccLvl)

            cuttedCharAccLvl = cuttedAccLvl[1:cuttedAccLvlRaw.start() - 4]

            newUser = User()
            newUser.id=cuttedCharId
            newUser.name=cutteCharName
            newUser.side=cuttedCharSide
            newUser.lvl=cuttedCharLvl
            newUser.accLvl=cuttedCharAccLvl
            Users.append(newUser)


fillUsersArray()

def check_character(id):
    objects = vk_user_session.method('board.getComments',  {'group_id': 118649434, 'topic_id': 47958603})
    if str(id) in str(objects) : return True
    else: return False

def getCurUserState(id):
    for user in Users:
        if user.id == id:
            return user.State

def setCurUserState(id,state):
    for user in Users:
        if user.id == id:
            user.State = state
            return


def make_new_playerboard_msg(id,name,side):
    if  check_character(id):
        sender(id,"У тебя уже есть персонаж!")
    else:
        message = "1) Имя персонажа :"+ name+ " \n 2) Код персонажа: " + str(id)+ "\n 3) Валюты: ОЗУ - 0, колл - 0 \n 4) Игровой уровень: 1 | Уровень аккаунта : 0 \n 6)Раса: \n 7) Инвентарь:"+"\n 8) Сторона :"+side
        vk_user_session.method('board.createComment',{'group_id':118649434,'topic_id':47958603,'message':message,'from_group':1})


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def sender (id,text,keyboard = ""):
    if keyboard == "" :
        vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard})
def getUserCharacter(id):
    for user in Users:
        checkUser = User()
        checkUser.id=id
        newStr =str(id)[0:]
        if str(str(user.id)[1:]) == str(newStr):
            return user
        else:continue
    return False

def getUserCharacterString(user):
    string = "1) Имя: "+user.name +" \n 2)Игровой уровень: "+str(user.lvl) + " | Уровень аккаунта: "+str(user.accLvl)+" \n 3)Сторона: "+user.side
    return string
def displayMenu():
    keyboard = {
        "one_time": True,
        "buttons": [
            [get_but('Оставить заявку на начисление ОЗУ💬', 'positive')],
            [get_but('Проверить своего персонажа 😎', 'positive')],
            [get_but('Открыть магазин 🧮', 'positive')]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    sender(id, "Чем хочешь заняться?", keyboard)
def send_some_mesage(id,text):
  if text == "Меню":
     displayMenu()
  elif (text == "Начать"):
      if check_character(id):
          sender(id, "У тебя уже есть аккаунт!")
          displayMenu()
      else:
          keyboard = {
              "one_time": True,
              "buttons": [
                  [get_but('Начать регистрацию', 'positive')],
                  [get_but('Помощь', 'positive')]
              ]
          }
          keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
          keyboard = str(keyboard.decode('utf-8'))
          sender(id,
                 "По всей видимости ты здесь новенький. Готов создать своего персонажа и начать покорение Айнкрада?",
                 keyboard)
          newUser = User();
          newUser.id = id;
          Users.append(newUser)
          pprint(Users)
          print("---------------------------------------")

  elif text.startswith("Проверить своего персонажа"):
      print("Начинаю проверку")
      if getUserCharacter(id) != False:
          print("Не пустой")
          sender(id,"Вот твой персонаж: \n"+ getUserCharacterString(getUserCharacter(id)))
          send_some_mesage(id,"Меню")
      else:
          print("Пустой")
  elif (text == "Оставить заявку на начисление ОЗУ💬"):

            sender( id, "Оформи заявку по следующей форме и отправь сюда: \n|НАЧИСЛЕНИЕ ОЗУ|\n 1)Имя персонажа\n 2)Кол-во ОЗУ\n 3)Ссылки-подтверждения на заработок ОЗУ")
  elif "|НАЧИСЛЕНИЕ ОЗУ|" in text:
            sender(id,"Отправили твою заявку ответственному человеку. Её рассмотрят в ближайшем времени и обновят данные!")
            sender(515721924, "1 Тебе новая заявка на зачисление ОЗУ! \n"+text +"\n пришла от пользователя с id: "+ str(id))
  else:
            sender( id,"Прости, я не знаю команды: "+text+". Напиши \"Меню\" чтобы перейти вернуться к главному экрану")



def registration(id,msg='',localstate =''):
    print(msg)
    print(localstate)
    if(check_character(id)):
        sender(id, "У тебя уже есть аккаунт!")
        displayMenu()
        return
    if(localstate == "Registration begin"):
          keyboard = {
            "one_time": True,
            "buttons": [
                [get_but('Я из SAO', 'positive')],
                [get_but('Я из UW', 'positive')]
            ]
                    }
          keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
          keyboard = str(keyboard.decode('utf-8'))
          sender(id,"Начнем с простого, на какой стороне ты находишься?",keyboard)



    if(localstate == "Recieved world"):
           sender(id, "Прекрасно! Интересненько... Как будут звать твоего персонажа?")
           for user in Users:
                print("Do cycle step")
                if user.id == id:
                    if (user.side == "SAO" or user.side == "UW"):
                        return True
                    else:
                        user.side = msg[5:]
                        return True
                else:
                    continue
           return False
    if(localstate == "Recieved name"):
        keyboard = {
            "one_time": True,
            "buttons": [
                [get_but('Да', 'positive')],
                [get_but('Нет, я хочу его изменить', 'negative')]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        sender(id, msg +"... Выбор этого имени является окончательным?",keyboard)

    if(localstate == "Complete Registration"):
        for user in Users:
            if user.id == id:
                user.name = msg
                make_new_playerboard_msg(user.id,user.name,user.side)


State = "null"
namemsg=''
for event  in longpool.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text
            id = event.user_id;
            if(msg == "Начать регистрацию"):
                setCurUserState(id,"Registration begin")
                registration(id,msg,getCurUserState(id))
            elif(msg=="Я из SAO" or msg == "Я из UW"):
                setCurUserState(id,'Recieved world')
                if registration(id,msg,getCurUserState(id)):
                    setCurUserState(id,  "Sended name pending")
                else:
                    setCurUserState(id,"Recieved world")
            elif(getCurUserState(id) == "Sended name pending"):
                setCurUserState(id, "Recieved name")
                registration(id,msg,getCurUserState(id))
                namemsg=msg;
            elif(getCurUserState(id) == "Recieved name" and str(msg).startswith("Нет")):
                setCurUserState(id,'Recieved world')
                if registration(id, msg, getCurUserState(id)):
                    setCurUserState(id, "Sended name pending")
                else:
                    setCurUserState(id, "Recieved world")
            elif(getCurUserState(id) == "Recieved name" and str(msg).startswith("Да")):
                    sender(id, "Прекрасно! Создаю твоего персонажа...")
                    setCurUserState(id, "Complete Registration")
                    registration(id,namemsg,getCurUserState(id))
                    setCurUserState(id, "null")
                    sender(id, "Ты можешь посмотреть свою анкету здесь: https://vk.com/topic-118649434_47958603")
                    send_some_mesage(id,"Меню")

            elif State =="null":
                send_some_mesage(id,msg)
