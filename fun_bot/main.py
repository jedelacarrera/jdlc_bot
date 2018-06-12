import random


FUN_FACTS = [
	"McDonalds calls frequent buyers of their food heavy users.",
	"The average person spends 6 months of their lifetime waiting on a red light to turn green.",
	"The largest recorded snowflake was in Keogh, MT during year 1887, and was 15 inches wide.",
	"You burn more calories sleeping than you do watching television.",
	"There are more lifeforms living on your skin than there are people on the planet.",
	"Southern sea otters have flaps of skin under their forelegs that act as pockets. When diving, they use these pouches to store rocks and food.",
	"In 1386 a pig in France was executed by public hanging for the murder of a child.",
	"One in every five adults believe that aliens are hiding in our planet disguised as humans.",
	"If you believe that you’re truly one in a million, there are still approximately 7,184 more people out there just like you.",
	"A single cloud can weight more than 1 million pounds.",
	"A human will eat on average 70 assorted insects and 10 spiders while sleeping.",
	"James Buchanan, the 15th U.S. president continuously bought slaves with his own money in order to free them.",
	"There are more possible iterations of a game of chess than there are atoms in the known universe.",
	"The average person walks the equivalent of three times around the world in a lifetime.",
	"Men are 6 times more likely to be struck by lightning than women.",
	"Coca-Cola would be green if coloring wasn’t added to it.",
	"You cannot snore and dream at the same time."
]


class FunBot(object):
	def __init__(self):
		pass

	def random(self):
		return "Did you know?\n" + random.choice(FUN_FACTS)
		