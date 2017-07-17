from gtpinterface import gtpinterface
from mctsagent import mctsagent
#from crit_mctsagent import crit_mctsagent
#from ext_crit_mctsagent import ext_crit_mctsagent
from rave_mctsagent import rave_mctsagent
#from miai_mctsagent import miai_mctsagent
def main():
	"""
	Main function, simply sends user input on to the gtp interface and prints
	responses.
	"""
	agent = rave_mctsagent()
	interface = gtpinterface("rave")
	success, response = interface.send_command("showboard")
	print(response + '\n')
	while True:
		command = raw_input()
		command1 = 'play black '+command
		success, response = interface.send_command(command1)
		print(("= " if success else "? ")+response+'\n')
		success, response = interface.send_command("showboard")
		print(response + '\n')
		success, response = interface.send_command("genmove white")
		print(("= " if success else "? ") + response + '\n')
		success, response = interface.send_command("showboard")
		print( response + '\n')

if __name__ == "__main__":
	main()
