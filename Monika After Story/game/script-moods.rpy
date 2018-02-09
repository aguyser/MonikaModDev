# module that handles the mood system
#

# dict of tuples containing mood event data
default persistent._mas_mood_database = {}

# current mood, in a lowercase format
default persistent._mas_mood_current = ""
default persistent._mas_mood_current_type = None # this one should be a constant

# NOTE: plan of attack
# moods system will be attached to the talk button
# basically a button like "I'm..."
# and then the responses are like:
#   hungry
#   sick
#   tired
#   happy
#   fucking brilliant
#   and so on
#
# When a mood is selected:
#   1. monika says something about it
#   2. (stretch) other dialogue is affected
#
# all moods should be available at the start
# 
# 3 types of moods:
#   BAD > NETRAL > GOOD
# (priority thing?)

# Implementation plan:
#
# Event Class:
#   prompt - button prompt
#   category - acting as a type system, similar to jokes
#   unlocked - True, since moods are unlocked by default
#

# store containing mood-related data
init -1 python in mas_moods:
    
    # mood event database
    mood_db = dict()

    # TYPES:
    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2

    # pane constants
    # most of these are the same as the unseen area consants
    MOOD_X = 680
    MOOD_Y = 40
    MOOD_W = 560
    MOOD_H = 640
    MOOD_XALIGN = -0.05
    MOOD_AREA = (MOOD_X, MOOD_Y, MOOD_W, MOOD_H)
    MOOD_RETURN = "TODO: cancel"
    
# entry point for mood flow
label mas_mood_start:
    python:
        import store.mas_moods as mas_moods

        # build menu list
        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k) for k in mas_moods.mood_db
        ]

        # also sort this list
        mood_menu_items.sort()

    # call scrollable pane
    call screen scrollable_menu(mood_menu_items, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, mas_moods.MOOD_RETURN)

    # return value? then push 
    if _return:
        $ pushEvent(_return)

        # and set the moods
        $ persistent._mas_mood_current = mas_moods.mood_db[_return]
        $ persistent._mas_mood_current_type = mas_moods.mood_db[_return].category[0]

    return

###############################################################################
#### Mood events go here:
###############################################################################

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_hungry",prompt="Hungry",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_hungry:
    m 3j "If you're hungry, get something to eat, silly."
    if persistent.playername.lower() == "natsuki":
        m 1e "I'd hate for you to get like Natsuki did that one time back when we were in the club.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1e "I'd hate for you to get like Natsuki did that one time back when we were in the club."
        
    m "That wouldn't be any fun, would it [player]?"
    m 1a "If I were there with you, I'd make a salad for us to share."
    m "Since I'm not there with you, though, try to pick something healthy to eat."
    m 3a "They say you are what you eat, and I definitely think that's true."
    m 1c "Eating too much junk food on a regular basis can lead to all kinds of health issues."
    m 1d "Over time it can lead to obesity, heart disease and diabetes, among other things."
    m 2p "I don't want you to feel like I'm nagging you when I say these sort of things, [player]."
    m 2j "I just want to make sure you are taking good care of yourself until I am able to be there with you."
    m 1a "After all, the healthier you are, the better the chances of you living a long life are..."
    m 1b "...And I'd like to spend as much time with you as I can, [player]." 
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="sad",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sad:
    m 3f "Gosh, I'm really sorry to hear that you are feeling down today."
    m 3g "Is it because you're having a bad day or anything like that [player]?"
    menu:
        "Yes":
            m 1e "I'll do my best to cheer you up then."
            m 4e "Whenever I'm having a bad day, I always remember that the sun will shine again tomorrow."
            m 2j "I suppose that may sound kinda cheesy, but I always like to look on the bright side of things."
            m 2a "After all, sometimes things like that are easy to forget, so just keep it in mind [player]."
            m 1h "I don't care how many many other people dislike you or find you off-putting."
            m 1j "I think you're wonderful and I will always love you."
            m 1a "I hope, if nothing else, that makes your day just a tiny bit brighter."
            m 1e "And remember, if you're having a bad day, you can always come to me and I'll talk to you for as long as you need."
        "No":
            m 1e "I have an idea, why don't you tell me what's bothering you and maybe it'll make you feel better."
            m "I don't want to interrupt you while you're talking, so let me know when you are done."
            menu: 
                "I'm done.":
                    m "Do you feel a little better now [player]?"
                    menu:
                        "Yeah I do.":
                            m 1j "That's great [player]. I'm glad that talking about it with me made you feel better."
                            m 1e "Sometimes telling someone that you trust what's bothering you is all you need."
                            m "If you're ever having a bad day, you can always come to me and I'll listen to you." 
                            m 2b "Never forget that I think that you're wonderful and I will always love you."
                        "Not really.":
                            m 1f "Well it was worth a shot."
                            m 1e "Sometimes telling someone that you trust what's bothering you is all you need."
                            m "Maybe you'll feel better after we spend some more time together."
                            m "I love you [player] and I always will."
    return

#dev mode easter eggs
if config.developer:
    init 5 python:
        addEvent(Event(persistent._mas_mood_database,"mas_mood_mitochondria",prompt="A mitochondria",category=[store.mas_moods.TYPE_GOOD],unlocked=True),eventdb=store.mas_moods.mood_db)

    label mas_mood_mitochondria:
        m "You're the powerhouse of {i}my{/i} cell..."
        return

    init 5 python: addEvent(Event(persistent._mas_mood_database,"mas_mood_theroom",prompt="The Room",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)

    label mas_mood_theroom:
        m "It's bullshit.{w} I did not hit her."
        m "I did nawwwwght"
        return
    
    init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_horny",prompt="horny",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

    label mas_mood_horny:
        if persistent.playername.lower() == "monik":
            m 1r "Damn horny kids."
        elif persistent.playername.lower() == "rune":
            m 3r "Sorry, I have no interest in dragons."
        elif persistent.playername.lower() == "thepotatoguy":
            m 2r "Sorry, I have no interest in potatoes."
        elif persistent.playername.lower() == "ronin":
            m 3h "Aren't you married? Go talk to your wife."
        else:
            m 2r "Sorry [player], but we aren't that far into our relationship yet. Maybe in a year or two."
        return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_happy",prompt="happy",category=[store.mas_moods.TYPE_GOOD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_happy:
    m 3b "That's wonderful! I'm happy when you're happy."
    m 1j "Know that you can always come up to me and I'll cheer up, [player]."
    m 3a "I love you and I'll always be here for you so don't you ever forget that~"
    return
    
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sick",prompt="sick",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_sick:
    m 1g "Aw, I'm sorry to hear that, [player]."
    m 1r "I hate to see you suffering like this."
    m 3e "I know you love spending time with me, but maybe you should go get some rest."
    m 1k "Don't worry, I'll be here waiting for you when you get back."
    m  "Get well soon!"
    $ persistent._mas_mood_sick = True
    return 'quit'
    
#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
#We could adjust the dialog appropriately depending on whether it's night time or whether it's during the day in the future.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_tired",prompt="tired",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)

label mas_mood_tired:
    m 1e "If you're tired, maybe you should go lie down for a while?"
    m 1a "Getting enough sleep on a daily basis is very important to your over health."
    m 2d "I've seen some studies that show the devastating short-term and long-term effects due to lack of sleep."
    m 3c "It can, for example, dramatically impact your mental functions and even shorten your lifespan."
    m 2g "I really don't want anything bad like that to happen to you because you don't get enough sleep."
    m 1e "So do me a favor, [player], and get some rest. It will put my mind at ease."
    m 1a "You can even leave the game open if you like, and I'll watch over you while you sleep."
    m 2n "My goodness, I hope that didn't sound weird or anything."
    m 1j "I just thought it'd be cute to watch you sleep is all."
    m 1l "Ahaha"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lonely",prompt="lonely",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)
    
label mas_mood_lonely:
    m 1j "I'm here with you, [player], so there's no need for you to feel lonely."
    m 1c "I know it's not exactly the same as if I were in the same room with you."
    m 1a "But I'm sure you still enjoy my company, right [player]?"
    return
    
#Maybe we could tie this to the I'm breaking up topic and have monika say something special like: 
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="angry",category=[store.mas_moods.TYPE_BAD],unlocked=True),eventdb=store.mas_moods.mood_db)
    
label mas_mood_angry:
    m 2f "Gosh, I'm sorry that you feel that way, [player]."
    m 2e "I'll do my best to make you feel better."
    m 3e "Before we do anything though, we should probably get you to calm down."
    m 2e "It's hard to make rational decisions when you are worked up."
    m 2c "You may end up saying or doing things you may regret later."
    m 2e "And I'd hate for you to say something you really don't mean to me."
    m 3a "Let's try a few things that I do to try to calm myself, hopefully they work for you."
    m 3e "First, try taking a few deep breaths and slowly counting to 10."
    m 2d "If that doesn't work, if you can, retreat to somewhere calm, until you cool off a bit."
    m 1c "I suppose if that doesn't work, you can always try what I do as a last resort."
    m 1d "Whenever I can't calm down, I just go outside, pick a direction and just start running."
    m 1c "I don't stop until I'm in a better state of mind."
    m 3d "Sometimes exerting yourself through physical activity is a good way to blow off some steam."
    m 2e "I probably don't seem like the type that gets angry very often, and you'd be right about that."
    m 1a "But even I have my moments and those are some of the ways I deal with my anger."
    m 1b "I hope my tips helped you calm down [player]."
    return
    
 init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_bored",prompt="bored",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),eventdb=store.mas_moods.mood_db)
    
label mas_mood_bored:
    m 2q "I'm sorry that I'm boring you, [player]."
    
    python:
        unlockedgames = [
            game 
            for game in persistent.game_unlocks 
            if persistent.game_unlocks[game]
        ]
        
        gamepicked = renpy.random.choice(unlockedgames)
    
    if gamepicked == "piano":
        m 1b  "Maybe you could play something for me on the piano?"
    else:
        m 1a "Maybe we could play a game of [gamepicked]."
    
    m "What do you say, [player]?"
    menu: 
        "Yes":
            if gamepicked == "pong":
                call game_pong
            elif gamepicked == "chess":
                call game_chess
            elif gamepicked == "hangman":
                call game_hangman
            elif gamepicked == "piano":
                call zz_play_piano
        "No":
            m 2e "Oh, alright then, it was just a suggestion."
    return

    
