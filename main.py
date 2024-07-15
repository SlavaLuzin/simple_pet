from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from random import choice, randint
from g4f.client import Client
from g4f.Provider import GeminiProChat
 
class MainApp(App):
	def __init__(self):
		super().__init__()
		self.mood = 100
		self.eyes = 1
		self.eyes_closing = False
		self.main()

	def main(self):
		self.morgch = "0"*90+"1"*10
		chance_of_gpt = 7
		self.gptch = "0"*(100-chance_of_gpt)+"1"*chance_of_gpt
		self.face = Image(source=self.get_face_img())
		self.resp = Label(text="", size_hint_y=.3)
		self.inp = TextInput(multiline=True, on_text_validate=self.listen, size_hint_y=.2)
		self.sendbtn = Button(text="OuO", size_hint_y=.2, size_hint_x=.1)
		self.sendbtn.bind(on_press=self.listen)
		self.lay = BoxLayout(orientation="vertical")
		self.textlay = BoxLayout(orientation="horizontal", padding=0)
		self.lay.add_widget(self.face)
		self.lay.add_widget(self.resp)
		self.textlay.add_widget(self.inp)
		self.textlay.add_widget(self.sendbtn)
		self.lay.add_widget(self.textlay)
		Clock.schedule_interval(self.morgat, 0.1)
	
	def build(self):
		self.icon = "faces/basic_smile.jpg"
		self.title = "Пушок"
		return self.lay
	
	def morgat(self, *args):
		if choice(self.morgch) == "1":
			Clock.schedule_once(self.morgat_two, 0.1)
		mor = choice(f"{'0'*(100-24)}{'1'*12}{'2'*12}")
		if mor == "1":
			r = randint(0, 10)
			if not self.mood+r > 110:
				self.mood += r
		elif mor == "2":
			r = randint(0, 10)
			if not self.mood-r < 0:
				self.mood -= r

	def morgat_two(self, *args):
		if self.eyes_closing:
			if self.eyes == 3:
				self.eyes = 2
				self.face.source = self.get_face_img()
				return 1
			elif self.eyes == 2:
				self.eyes = 1
				self.eyes_closing = False
				self.face.source = self.get_face_img()
				return 1
		else:
			if self.eyes == 1:
				self.eyes = 2
				self.face.source = self.get_face_img()
				return 1
			elif self.eyes == 2:
				self.eyes = 3
				self.eyes_closing = True
				self.face.source = self.get_face_img()
				return 1

	def get_face_img(self):
		if self.mood in range(0, 46):
			if self.eyes == 1:
				return "faces/basic_grust.jpg"
			elif self.eyes == 2:
				return "faces/clo_grust.jpg"
			elif self.eyes == 3:
				return "faces/closed_grust.jpg"
		elif self.mood in range(45, 56):
			if self.eyes == 1:
				return "faces/basic_basic.jpg"
			elif self.eyes == 2:
				return "faces/clo_basic.jpg"
			elif self.eyes == 3:
				return "faces/closed_basic.jpg"
		elif self.mood > 100:
			return "faces/recs.jpg"
		else:
			if self.eyes == 1:
				return "faces/basic_smile.jpg"
			elif self.eyes == 2:
				return "faces/clo_smile.jpg"
			elif self.eyes == 3:
				return "faces/closed_smile.jpg"

	def listen(self, *args):
		if self.mood in range(0, 46):
			moodstr = "грустный"
		elif self.mood in range(45, 56):
			moodstr = "нормальное"
		elif self.mood in range(55, 101):
			moodstr = "весёлый"
		else:
			moodstr = "удивлённый"
		l = self.inp.text
		prompt = f'''
		Ты являешься моим виртуальным питомцем по имени Пушок.
		Ты должен отвечать короткими фразами, которые соответствуют твоему настроению.
		Твоё настроение: {moodstr}
		Ты должен вести себя как питомец.
		Придумай ответ на фразу пользователя: "{l}" (если фраза пользователя пустая, тогда придумай случайную фразу)'''
		response = gpt.chat.completions.create(
			provider=GeminiProChat,
			model="gpt-3.5-turbo",
			messages=[{"role": "user", "content": prompt}]
		)
		self.resp.text = response.choices[0].message.content
 
if __name__ == '__main__':
	gpt = Client()
	app = MainApp()
	app.run()