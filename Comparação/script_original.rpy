# The script of the game goes in this file.



init:
    $ config.window_title = "Beachfront 0.7"

    # Set this to true to enable some developer-specific
    # functionality. It should be false in a finished game.
    # Read the "Developer Tools" section of the reference
    # to see what this enables.
    $ config.developer = True

## Abans de compilar i publicar
#   1 Moure "$ MainMenu(confirm=False)()" al darrer dia
#   2 Assgurar-se que el joc comença del principi i acaba al final33



    python:

        import math

        class Shaker(object):

            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }

            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child

            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor

                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)

        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)

            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)
    #

#





# Declare characters used by this game. The color argument colorizes the
# name of the character.

define w = Character("Alina",color="008080")
define u = Character("?????",color="008080")
define ga = Character("")
define r = Character("Rachel",color="#008000")
define l = Character("Lucy",color="#800000")
define ge = Character("George",color="#0000ff")
define c = Character("Claudia",color="#ff00ff")
define mc = Character("Alan")
define mab = Character("Mabel", color="#4169e1")
define sar = Character("Sara", color="#98fb98")
define cryst = Character("Crystal", color="#9932cc")
define milf = Character("Claudia",color="#ff0000")
define da = Character("Dana", color="#ff4040", what_color="#ffffff")
define na = Character("Naomi", color="#4b0082")
define oldman = Character("Oldman", color="#4b0082")
define youngman = Character ("Boy", color="008080")
define nurse = Character ("Nurse", color="008080")

define musica1="/audio/Beachside Dreams-1.mp3"
define musica2="/audio/Beachside Dreams-2.mp3"
define musica3="/audio/Emphemeral Dreams-1.mp3"
define musica4="/audio/Emphemeral Dreams-2.mp3"
define musica5="/audio/Whispering Shores.mp3"
define musica6="/audio/bellydance.mp3"
define musica_intro="/audio/intro.mp3"
define musica_strip="/audio/strip02.mp3"
define beach="/audio/beachfront.mp3"


define lust = 0
define alina = 0
define claudia = 0
define lucy = 0
define crystal = 0
define sara = 0
define mabel = 0
define rachel=0
define player_sara="daddy"


#image mymovie= Movie(play="dance.webm")
#image first = Movie(play = "claudia.webm")
image myvideo = Movie(play="/images/claudia.webm", loop=True)
#image animation = Movie(channel="movie_dp", play="claudiabj.mp4")

image lucy_video = Movie(play="images/lucy3.webm", loop=True)

# The splashscreen is called, if it exists, before the main menu is
# shown the first time. It is not called if the game has restarted.

# We'll comment it out for now.
#
#label splashscreen:
#     scene black
#     show text "American Bishoujo Presents..." with fade
#     $ renpy.pause(0.1)
#     hide text with fade
#
#     return


default persistent.dialogueBoxOpacity = 1.0

# The game starts here.

label start:

    #centered "First of all, thanks fro playing my game!"
    centered "\n\nAll characters depicted in this game are 18 and older"
    #after centered, use extend
    call age_verification_prompt from _call_age_verification_prompt

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    # These display lines of dialogue.

    $ player_name = renpy.input("What is your name (default is Alan)?")

    $ player_name = player_name.strip()

    # The .strip() instruction removes any extra spaces the player
    # may have typed by accident.

    #  If the player can't be bothered to choose a name, then we
    #  choose a suitable one for them:
    if player_name == "":
        $ player_name="Alan"
    $ mc = Character(player_name,color="#ff0000")

    # Now the other characters in the game can greet the player.

    ga "Pleased to meet you, %(player_name)s! Thanks for playing my game."

    #call d7alina_end
    #call d7rachel_end
    #call d7crystal_end
    #call d7claudia_end
    #call d7mabel_end
    call introduction from _call_introduction
    call day1 from _call_day1
    call day2 from _call_day2
    call day3 from _call_day3
    call day4 from _call_day4
    call day5 from _call_day5
    call day6 from _call_day6

label after_load:


#This ends the game
return

label day1:
    scene day1 with dissolve
    pause 5.0
    call waiting from _call_waiting
    call apartment from _call_apartment
    call alina from _call_alina
    call night1 from _call_night1
    return

label day2:
    scene day2 with dissolve
    call tothebeach from _call_tothebeach
    call mabel from _call_mabel
    call sara from _call_sara
    call ice_cream from _call_ice_cream
    call bar_scene from _call_bar_scene
    return

label day3:
    scene day3 with dissolve
    call topless from _call_topless
    call apart3 from _call_apart3
    call jacuzzi from _call_jacuzzi
    return


label day4:
    scene day4 with dissolve
    call morning4 from _call_morning4
    #call crystal_out
    #call alina_out
    call afternoon4 from _call_afternoon4
    call night4 from _call_night4
    #call end4 from _call_end4

    return


label day5:
    scene day5 with dissolve
    call morning5 from _call_morning5
    call cinema5 from _call_cinema5
    call evening5 from _call_evening5
    call d5apart from _call_d5apart
    #call end5 from _call_end5
    return

label day6:
    scene day6 with dissolve
    call morningd6 from _call_morningd6
    call beachd6 from _call_beachd6
    call mabeld6 from _call_mabeld6
    call d6beach2 from _call_d6beach2
    call d6ice from _call_d6ice
    call d6bar from _call_d6bar
    call decission from _call_decission
    return


label d7claudia_end:
    scene black with dissolve
    centered "What a normal day with Claudia looks like..."

    scene d7claudia005 with dissolve
    c "Thank you…For choosing me. For coming with me today."

    scene d7claudia010 with dissolve
    c "It means a lot… that you want to go to the beach together. Just us."
    mc "Of course I do."

    c "Still… thank you."

    scene d7claudia015 with dissolve
    c "Do you like my outfit for the beach today?"
    mc "Yes. I do… though it’s a bit revealing."

    scene d7claudia020 with dissolve
    c "Only a bit?"

    scene d7claudia025 with dissolve
    c "I want to put on a show for them… for everyone on this bus."

    scene d7claudia035 with dissolve
    c "Today is your lucky day… I’m so happy I finally started a relationship with [player_name], and I want to show all of you just how happy I am."

    scene d7claudia050 with dissolve

    oldman "My god… those tits of yours are incredible."

    c "You like them?"

    #scene d7claudia050 with dissolve
    #c "They’ve always been big… but I like when people notice."

    #oldman "Hard not to notice something like that."


    scene d7claudia060 with dissolve
    c "See? Heavy… soft…"
    youngman "Wow…"


    scene d7claudia075 with dissolve
    c "Should I…? I think I will."


    scene d7claudia080 with dissolve
    youngman "Holy shit… those are fucking huge. Look at how heavy they are."
    da "They’re… real, aren’t they?"

    scene d7claudia081 with dissolve
    da "They’re beautiful. Really. Mine never looked like that."
    scene d7claudia082 with dissolve
    c "Yours look nice too. Different… but nice."

    scene d7claudia085 with dissolve
    c "You’ve seen the top… but I think you deserve the full view."


    scene d7claudia083 with dissolve
    c "No panties… nothing underneath. Just me."
    oldman "Good lord…"
    youngman "Fucking hell… look at her. Not a single stitch left."


    scene d7claudia089 with dissolve
    c "This is my stop… I have to get off here."
    oldman "Already? What a shame…"
    youngman "Come on… just a few more minutes. Please."
    da "Wow! Thanks for the show"


    scene d7claudia091 with dissolve
    c "Did you enjoy the show [player_name]…?"

    menu:
        "Yes. I loved every second of it.":
            mc "Yes. I loved every second of it."
            scene d7claudia091_6 with dissolve
            c "I’m so glad…I wanted you to like it too."

        "No… it was too much.":
            mc "No… it was too much."
            scene d7claudia091_3 with dissolve
            c "Oh…I’m sorry if it was too much for you. But this is who I am… and who I’ll keep being."



    scene d7claudia095 with dissolve
    c "Come on, hop off with me. Let's go to the beach!"

    scene d7claudia100 with dissolve
    c "You’re staring again…"

    scene d7claudia105 with dissolve
    c "I can feel your eyes on me… on my tits… on everything."

    scene d7claudia110 with dissolve
    c "You know, it turns me on when you look at me like that."

    scene d7claudia139_2 with dissolve
    c "Don’t just stand there getting hard in your clothes, baby… Take it all off.I want to see you… all of you… "


    scene d7claudia141 with dissolve
    c "Oh… look at that. You’re so hard for me already… fuck, that’s hot."


    scene d7claudia127 with dissolve
    c "Feel how warm you are… throbbing in my hand."

    scene d7claudia125 with dissolve
    c "Mmm… I love how veiny you are. Feels so good on my tongue."


    #c "Mmmph… so thick…"


    scene d7claudia130 with dissolve
    c "Tastes so good… mmm…"

    scene d7claudia135 with dissolve
    #c "Mmmph… hard for me… so fucking hard…"

    c "Mmmph…"
    mc "Fuck… your mouth feels incredible."

    #c "Look at you throbbing on my tongue. You love it when I suck you out in the open like this, don’t you?"

    #mc "(breathing heavier) Yeah… I do. Especially knowing anyone could walk by."

    # She takes him back into her mouth, bobbing her head with more hunger, one hand squeezing her own heavy breast.
    scene d7claudia125 with dissolve
    c "Mmmph… taste so fucking good…"


    # After a while she pulls off and pushes him down onto the sand.
    scene d7claudia145 with dissolve
    c "My turn. I’m going to ride this cock until my legs shake."
    mc "Jesus, Claudia… you’re so wet already."

    # She sinks down onto him in one smooth motion, taking him deep.
    scene d7claudia155 with dissolve
    c "Fuuuck… there it is. Filling me up just the way I like."
    mc "You’re taking every inch so easily…"

    scene d7claudia160 with dissolve
    c "Watch them bounce for you. You like that, don’t you? My fat tits bouncing while I use your cock."

    $ renpy.movie_cutscene("images/claudia2.webm", loops=2, delay=None)

    scene d7claudia160 with dissolve
    mc "They look amazing when you ride me like this."


    scene d7claudia200 with dissolve
    c "Fuck… I’m getting close. Your cock is hitting me so deep…"
    mc "Me too… don’t stop riding me."


    scene d7claudia210 with vpunch

    c "YES!! Right there! I’m gonna cum all over your cock—!"
    scene d7claudia210 with hpunch
    scene d7claudia210 with dissolve
    mc "Claudia… I’m cumming—!"

    # Both of them reach the edge at the same time.

    scene d7claudia215 with dissolve
    c "Ahh—fuck! I’m cumming—!"
    mc "TAKE IT! —all of it—!"

    scene d7claudia170 with dissolve
    c "Fuck… that was intense. My legs are still shaking."
    mc "You look happy."


    scene d7claudia175 with dissolve
    c "Of course I’m happy. I just got fucked properly on the beach and came hard on your cock. What’s not to like?"
    mc "Fair point."


    scene d7claudia176 with dissolve
    c "I like having a man who can handle me. Keep treating me like this and I might get spoiled. Not that I’m complaining."
    mc "Good. I like seeing you like this."

    jump end

    return

label d7mabel_end:

    scene black with dissolve
    centered "What a normal day with Mabel (and Sara) looks like..."

    scene d7mabel010 with dissolve
    mab "Come on, [player_name]. Don’t just stand there looking at us."
    sar "Yeah… the court is all ours for now."


    scene d7mabel020 with dissolve    # Scene 2
    sar "Actually… I want to team up with you, [player_name]. Let’s play against Mom."

    scene d7mabel025 with dissolve
    mab "Oh? You think the two of you can beat me?"

    # Scene 3

    scene d7mabel075 with dissolve
    mab "Fine. Let’s make it interesting. The losers have to walk all the way from the court to the locker room… completely naked."
    scene d7mabel085 with dissolve
    sar "Deal! With [player_name] on my side, we’re definitely going to win."

    # Scene 4
    scene d7mabel025 with dissolve
    mab "Ready, [player_name]? Don’t go easy on me just because I’m your girlfriend."
    mc "Wouldn’t dream of it."

    # Scene 5
    scene d7mabel030 with dissolve
    mab "Here it comes!"

    # Mabel’s serve. Her short top shifts during the motion, causing a brief wardrobe malfunction that exposes more of her large breasts.

    # Scene 5 (continued)
    scene d7mabel035 with dissolve
    sar "[player_name]! Focus on the ball, not on Mom’s tits!"

    # Scene 6
    # Mabel lunges for a wide shot but can’t quite reach it, stumbling as she tries.
    scene d7mabel045 with dissolve
    mab "Damn it… almost had it!"

    # Scene 7
    # Sara returns a strong shot. As she swings, her short tennis skirt flips up, briefly showing her underwear (or lack of it).
    scene d7mabel055 with dissolve
    sar "Got it!"

    # Scene 7 (continued)
    scene d7mabel060 with dissolve
    sar "We win! Yes!"

    scene d7mabel070 with dissolve
    mab "Okay… okay, you two win. I lost fair and square."

    # Scene 8
    scene d7mabel090 with dissolve
    mab "Congratulations. You played really well… especially you, [player_name]."

    scene d7mabel095 with dissolve
    sar "Thanks for paying attention to the game and not getting too distracted."

    # Scene 10
    # Mabel starts walking toward the building, already beginning to undress as she leaves the court.
    scene d7mabel106 with dissolve
    mab "A bet’s a bet. No point waiting until we’re inside."

    # Scene 11
    scene d7mabel107 with dissolve
    mab "I’ll see you outside after I shower and change. Don’t take too long."

    scene black01 with dissolve
    centered "A few minutes later..."

    scene d7mabel209 with dissolve
    mab "[player_name]… the locker room is completely empty right now. Why don’t you come in? There’s a little surprise waiting for you."

    scene d7mabel210 with dissolve
    sar "Mmm… your nipples are so hard…"

    $ renpy.movie_cutscene("/images/nipples.webm")

    scene d7mabel210 with dissolve
    mab "That’s it, baby… keep going. He’ll be here any second."


    scene d7mabel225 with dissolve
    mc "{i}(Holy shit… they’re both completely naked and kissing each other like that. This is hotter than I expected.){/i}"


    scene d7mabel230 with dissolve
    mc "Looks like I didn’t need to rush after all. You two started without me."

    scene d7mabel235 with dissolve
    mab "There you are… we were wondering how long you’d take."
    sar "Hi, [player_name]… come closer."

    # Scene 2
    # Sara moves behind Mabel and begins gently playing with her large breasts, squeezing and caressing them while Mabel keeps her eyes on MC.

    scene d7mabel240 with dissolve
    mab "Mmm… she can’t keep her hands off me."
    mc "I can see that. You’re both already having fun without me."
    # Scene 3
    # Mabel and Sara turn their heads toward each other, sharing a heated look.

    scene d7mabel245 with dissolve
    mab "Ready?"
    sar "Yes…"



    scene d7mabel250 with dissolve    # Scene 4
    mab "Follow us."

    #sar "(taking MC’s hand lightly) Come here…"

    # They lead him a few steps deeper into the locker room.

    # Scene 5
    # Both women drop to their knees in front of MC. Sara wraps her hand around his shaft while Mabel watches her closely.

    scene d7mabel300 with dissolve
    sar "Mmmm, you’re already so hard…"
    mab "Good girl… show him how much you want him."
    mc "You two look so good like this."

    # Scene 6
    # Sara leans in and begins pleasing him orally, taking him into her mouth slowly while Mabel watches with clear excitement.

    scene d7mabel310 with dissolve
    sar "Mmm…"
    mab "That’s it… take him deeper."
    mc "Fuck… that feels amazing, Sara."
    # Scene 7
    # Sara continues, bobbing her head a little faster, one hand stroking the base.
    scene d7mabel320 with dissolve
    sar "slurp… mmm…"
    mc "Just like that…"
    # Scene 8
    # She keeps going, eyes flicking up toward MC from time to time while Mabel gently strokes Sara’s hair.
    scene d7mabel330 with dissolve
    sar "Mmmph… so thick…"
    # Scene 9
    scene d7mabel335 with dissolve
    mab "Now… you’re going to have to make a difficult decision, [player_name]."
    mc "A difficult decision? This should be interesting."

    scene d7mabel340 with dissolve
    mab "So, [player_name]… which one of us are you going to fuck?"
    sar "We’re both ready for you…"

    menu pussy_choice:
        "Choose Sara":
            scene d7mabel365 with dissolve
            mc "I’m taking you, Sara."

            #sar "(soft gasp) Okay… please…"

            scene d7mabel345 with dissolve
            mab "Good choice. Be gentle with her… or don’t. She can take it."
            sar "Ahh… you’re so deep already…"

            #mab "(voice husky, feeling Sara’s body move beneath her) Mmm… I can feel everything you’re doing to her."

            # The scene continues with MC thrusting into Sara while Mabel stays on top, both women moaning.


            scene d7mabel375 with dissolve
            sar "Ahh—I’m coming—!"

            # Sara climaxes hard while still on all fours under Mabel.

            mab "She already came… now I want you to finish on both of us."

            #sar "(still shaking, looking back at him) Yes… come on us… please…"

        "Choose Mabel":
            scene d7mabel360 with dissolve
            mc "I’m taking you, Mabel."
            #mab "(smiling back at him) Smart man. Come on then… fill me up."

            #sar "(from underneath, breathing faster) I can feel her getting ready for you…"


            scene d7mabel350 with dissolve
            mab "Fuck… yes… just like that…"
            sar "She’s so heavy on me… and I can feel every thrust…"

            scene d7mabel370 with dissolve
            mab "Fuck—I’m coming—!"
            sar "She already came… now we want you to finish on both of us. Please…"

            #mab "(still breathing heavily, smiling back at him) Yes… cover us both. Give us everything."


    # Scene 1
    scene d7mabel400 with dissolve
    #mab "Come on, [player_name]… finish on us. We both want it."
    sar "Please… cover us. I want to feel it on my face too."
    mab "Start with whichever one of us you want first. We’re ready."

    # Scene 2
    scene d7mabel410 with dissolve
    mc "I’ll start with you, Sara."
    sar "Yes…"

    # MC strokes himself and begins releasing the first thick ropes across Sara’s face.
    scene d7mabel421 with dissolve
    sar "Ahh… it’s so much…"

    mab "Look at that… painting her pretty face. Keep going, give her more."

    # Scene 3
    # After the first load covers Sara’s face, MC turns toward Mabel.
    scene d7mabel430 with dissolve
    mc "Your turn, Mabel."
    mab "I’m ready. Don’t hold back."

    # Scene 4
    # MC aims at Mabel and continues finishing, covering her face and chest while Sara watches.
    scene d7mabel441 with dissolve
    mab "Yes!… cover me. I love feeling your cum on my face."

    #sar "You’re covering Mom so much…"

    # Scene 5
    # Mabel stays on her knees, face and chest glistening, looking up at MC with clear love in her eyes.
    scene d7mabel460 with dissolve
    mab "…I love you. Seeing you like this, choosing to share this with us… it means everything."

    # Scene 6
    # Sara, still on her knees beside her, also looks up at MC with open affection.
    scene d7mabel470 with dissolve
    sar "Me too… I’m really happy you chose to be with us."

    # Scene 7
    scene d7mabel471 with dissolve
    mab "Thank you for choosing me, [player_name]. I promise I’ll be a good wife to you. I’ll take care of you… in every way you need."

    #stop music fadeout 2.0

    jump end
    return


label d7crystal_end:

    scene black with dissolve
    centered "What a day with Crystal looks like..."

    scene d7crystal015 with dissolve
    cryst "I still can’t believe you chose me… even knowing what I am. Most people would have walked away the moment they found out."
    mc "I chose you because of who you are, Crystal. Not in spite of it."

    scene d7crystal005 with dissolve
    cryst "That means more than you know. I’ve spent so long being afraid that no one would ever really want me."
    scene d7crystal010 with dissolve
    pause 2.0
    scene d7crystal020 with dissolve
    cryst "…You looked at them."
    mc "Crystal..."

    scene d7crystal026 with dissolve
    cryst "It’s ok… they have something I don’t. A real pussy. Soft and warm and… normal. Every time I see a woman like that, I can’t stop thinking that one day you’ll want that instead of me."
    mc "Crystal, stop. I knew exactly what you were when I chose you. I didn’t choose you by accident."


    scene d7crystal027 with dissolve
    cryst "What if one day you wake up and realize you want a real woman? Someone who can… feel like a woman in every way. I’m always going to be different."
    mc "Look at me. I like you as you are. The way you look, the way you feel, the way you are. I’m not waiting for you to become someone else. I chose {b}you{/b}."

    scene d7crystal028 with dissolve
    cryst "You really mean that…?"
    mc "Yes. I mean it."

    # Crystal is silent for a few seconds. Then a small, thoughtful smile appears on her lips.
    scene d7crystal040 with dissolve
    cryst "…Okay. Then maybe I have an idea."
    mc "What kind of idea?"

    scene d7crystal045 with dissolve
    cryst "Not yet. Just… trust me for now."

    scene black with dissolve
    centered "A few days later..."
    scene d7crystal100 with dissolve
    nurse "Good morning. You must be [player_name]. Please, come in."

    # They enter the room together. Crystal is still half-asleep under the sheet.

    scene d7crystal120 with dissolve
    nurse "The surgery went very well. Everything healed nicely. She’s recovering faster than expected."


    scene d7crystal130 with dissolve
    nurse "Crystal… your visitor is here."

    # As the nurse bends over the bed, her tight uniform stretches across her large, round ass, clearly visible to MC.

    scene d7crystal140 with dissolve
    nurse "She’s still out… good. Gives us a moment to talk."

    scene d7crystal150 with dissolve
    nurse "That new pussy of hers turned out even prettier than I expected. Soft, pink… already a little wet just from the recovery process."

    scene d7crystal160 with dissolve
    mc "It looks very natural."
    scene d7crystal170 with dissolve
    nurse "Mmm… it is. Honestly… That little slit looks so inviting."

    scene d7crystal180 with dissolve
    nurse "You’re a lucky man. She’s going to be so sensitive down there when she wakes up… and so eager to show you how good it feels."

    scene d7crystal190 with dissolve
    cryst "[player_name]… you’re here…"

    # Image 1

    scene d7crystal195 with dissolve
    nurse "Good morning, Crystal. How are you feeling after the surgery?"

    cryst "A little sore… but okay, I think."



    scene d7crystal240 with dissolve    # Image 2
    nurse "I need to check the sensitivity of the area. I hope you don’t mind that [player_name] is here watching."
    cryst "Of course I don’t mind… I want him to see."

    # Image 3
    # The nurse slowly pulls the sheet down and begins gently stroking Crystal’s cock, testing its response. It quickly hardens in her hand.

    scene d7crystal250 with dissolve
    nurse "Let’s see how this reacts…"
    cryst "Ahh… that feels… really sensitive…"

    # Image 4

    scene d7crystal255 with dissolve
    nurse "Everything seems more than okay. She hasn’t lost any sensitivity at all. If anything, it might be even more responsive now."

    # Image 4 (continued)
    scene d7crystal265 with dissolve
    $ renpy.movie_cutscene("images/crystal.webm", loops=2, delay=None)
    scene d7crystal265 with dissolve
    cryst "Nngh… don’t stop…"

    # Image 5
    # The nurse slides her other hand between Crystal’s legs and begins carefully fingering her new pussy while still groping one of Crystal’s breasts.
    scene d7crystal270 with dissolve
    nurse "Good reaction here too… very wet already."
    cryst "Oh god… "

    # Image 6
    # The nurse focuses on Crystal’s new clit, rubbing it in slow circles with her fingers while Crystal grows even wetter.
    scene d7crystal275 with dissolve
    nurse "There it is… your new little clit is very responsive. Look how wet you’re getting for us."
    cryst "Ahh—fuck… it feels so good…"

    scene d7crystal280 with dissolve
    cryst "[player_name]… do you want to try it? Feel how it reacts for you?"
    mc "Yes. I want it desperately."

    # Image 11
    scene d7crystal285 with dissolve
    cryst "Even here? In the hospital room… with the nurse still watching?"
    mc "I don’t mind. I want you right now."

    scene d7crystal290 with dissolve
    nurse "Then I want to participate too…"

    # She opens her uniform, revealing her huge, heavy breasts.
    scene d7crystal295 with dissolve
    nurse "I’ve been taking care of her for days… I think I’ve earned a turn."

    # Image 13
    # The nurse fully removes her uniform top.
    scene d7crystal300 with dissolve
    nurse "I’ll let you taste her new pussy first. I want to watch you do it."

    # Image 14
    # The nurse slides her panties down her full hips and steps out of them.
    scene d7crystal305 with dissolve
    nurse "And while you do that… I’ll take care of Crystal’s cock."

    # Image 15
    # The nurse is now completely nude, standing beside the bed, ready.
    scene d7crystal310 with dissolve
    nurse "Let’s give her a proper welcome to her new body."

    scene d7crystal330 with dissolve
    cryst "Please… put it in. I want to feel your cock inside my new pussy for the first time. Don’t make me wait any longer…"

    scene d7crystal335 with dissolve
    cryst "Ahh… it’s going in… so slowly… I can feel every bit of it…"
    mc "You’re so tight… and so wet already."

    scene d7crystal345 with dissolve
    nurse "Suck on them while he fucks your new pussy."

    scene d7crystal340 with dissolve
    cryst "Ahh—! I can feel it… your cock… inside my pussy… for the first time…!"

    scene d7crystal370 with dissolve
    nurse "That’s it… take him all the way in. How does it feel?"
    cryst "It’s so full… so different… and so fucking good…"

    # Scene 20
    scene d7crystal375 with dissolve
    mc "Crystal… I’m close. I’m going to come inside you…"
    #scene d7crystal376 with dissolve
    #cryst "Yes—do it. Fill my new pussy… I want to feel it…"

    # Scene 21
    # MC thrusts deep one last time and releases hard inside her.
    scene d7crystal380 with hpunch
    scene d7crystal380 with vpunch
    scene d7crystal380 with dissolve
    mc "Fuck..take it all!!"
 #   crystal "(crying out as she feels the hot pulses filling her) Ahh—! I can feel it… so much… so warm inside me…!"

    # Scene 22
    # At the same moment, both Crystal and the nurse reach their climax.
    scene d7crystal385 with dissolve
    cryst "AAAHHH! My new pussy is cumming around your cock!!"
    nurse "YES!!! ME TOO!"

    # All three ride out the intense shared climax.

    # Scene 23
    # Afterward, Crystal and the nurse are both on their knees on the floor in front of MC, looking up at him with satisfied, flushed faces.

    scene d7crystal390 with dissolve
    cryst "That was… incredible. I never imagined it could feel like that."
    nurse "You two were beautiful together. I almost came just from watching the way her new pussy took you."

    # Scene 24
    # Crystal stands up and wraps her arms around MC, hugging him tightly.
    scene d7crystal395 with dissolve
    cryst "Thank you… for everything. For choosing me. For staying. For making me feel this wanted."

    # Scene 25
    scene d7crystal399 with dissolve
    cryst "I’ll be with you forever. I’ll give you everything you want… everything you need. My body, my heart… all of it is yours."

    scene black with dissolve
    call end from _call_end
    return


label d7alina_end:
    scene black with dissolve
    centered "What a normal day with Alina looks like..."

    scene d7alina010 with dissolve
    mc "(thinking) {i}She’s here… cooking in our kitchen and almost naked...{/i}"

    scene d7alina020 with dissolve    # Image 2
    w "Welcome home. Dinner is almost ready."

    # She looks at him the way a devoted wife would — warm, calm, and clearly glad he’s back.

    # Image 3
    scene d7alina025 with dissolve
    w "I’m finished. You should get comfortable. Sit down, relax… you’ve been out all day."
    mc "I’d rather stay here with you for a bit. I’ve been looking forward to coming home to you."

    # Image 4
    # Alina lightly wipes the sweat from her forehead with the back of her hand, still wearing her apron.
    scene d7alina040 with dissolve
    w "How was your day? Was everything okay?"
    mc "It was fine… but this is the best part of it. Coming back and finding you here."

    # Image 5
    scene d7alina050 with dissolve
    w "Thank you… for choosing me. I still can’t believe I get to be the one waiting for you like this."
    mc "I chose you because this is what I wanted. Coming home to you… every day."

    # Image 6
    scene d7alina060 with dissolve
    w "I love being here with you… but sometimes I still wonder if I’m enough. The other women you met were so much prettier than me."

    mc "Alina. I didn’t choose them. I chose you. You’re the one I want."

    # Image 7
    scene d7alina070 with dissolve
    w "Do you… really find me attractive? Even compared to them?"
    mc "Yes. I find you beautiful. Exactly the way you are."

    # Image 8
    # Alina slowly starts untying her apron, her fingers a little nervous.
    scene d7alina080 with dissolve
    w "Then… let me show you."

    # She begins undressing the apron. MC waits quietly, watching her.

    # Image 9
    # Alina opens the top of the apron, revealing her bare breasts. She looks at MC, searching his face for acceptance.
    scene d7alina090 with dissolve
    w "…Do you still want me like this?"
    mc "Yes. I want you."

    # Image 10
    # Alina continues undressing, letting the apron slip further down her body.
    scene d7alina095 with dissolve
    w "Then… I’ll give you all of me."

    scene d7alina100 with dissolve
    w "I want you to take me, … please."
    mc "I will."

    # Image 11
    scene d7alina105 with dissolve
    w "Follow me."

    # She leads him a few steps away from the kitchen counter.

    # Image 12
    # Alina bends over the edge of the sofa / table, presenting herself to him.
    scene dtalina120 with dissolve
    w "Like this… I want to feel you inside me right here."

    # Image 13
    # MC is already hard. He steps closer, the tip of his cock resting against her entrance.
    scene d7alina130 with dissolve
    mc "You’re already so wet…"

    # Image 14
    # MC slowly pushes inside her.
    scene d7alina140 with dissolve
    w "Ahh… you’re in…"

    # Image 15
    scene d7alina150 with dissolve
    w "It feels so good… having you this deep inside me…"

    # Image 17
    # MC begins moving steadily. Alina pushes back to meet each thrust.
    scene d7alina160 with dissolve
    w "Yes… just like that… don’t stop…"

    # Image 18
    # They continue, the rhythm growing deeper and more intense.
    scene d7alina170 with dissolve
    w "I love feeling you… keep going…"

    scene d7alina180 with dissolve
    w "You’re so deep… I can feel every inch of you."

    scene d7alina190 with dissolve
    w "Ahh—! Like that… harder… please…"


    scene d7alina200 with dissolve
    mc "Alina… I’m getting close…"
    w "Take it out… please. I want you to cum all over me."


    scene d7alina210 with dissolve
    mc "You sure?"
    #scene d7alina220 with dissolve
    w "Yes… cover me. I want to feel it on my skin."

    # MC strokes himself and releases, thick ropes of cum landing across Alina’s lower back, ass, and thighs.
    scene d7alina230 with dissolve
    w "Mmm… there’s so much… it’s so warm…"
    scene d7alina240 with dissolve
    mc "Fuck… look at you."
    scene d7alina245 with dissolve
    w "I wanted this… to feel marked by you."
    scene d7alina250 with dissolve
    w "Thank you… for being my man. For choosing me."

    # She gives the tip a slow, gentle stroke with her thumb, wiping away the last traces of cum.
    scene d7alina255 with dissolve
    w "I still can’t believe this is real. That someone like you wanted me… and only me."
    scene d7alina260 with dissolve
    w "I’ll take care of you. Every day. I promise."
    scene d7alina265 with dissolve
    w "Mmm… even the last bit of you tastes so good. I don’t want to waste a single drop."
    scene d7alina270 with dissolve
    w "I want to be the perfect wife for you… proper and polite when we’re around other people, but completely naughty and shameless whenever we’re alone like this."

    scene black with dissolve
    call end from _call_end_1
    return

    return



label d7rachel_end:
    scene black with dissolve
    centered "What a normal day with Rachel (and Lucy) looks like..."

    scene d7rachel085 with dissolve
    r "Welcome home. How was your day? Did everything go alright?"
    scene d7rachel100 with dissolve
    l "Yeah, spill it. Was it boring, or did something actually interesting happen for once?"
    mc "It was pretty normal. Meetings, some work, nothing special. What about you two? How was your day?"

    #scene d7rachel110 with dissolve
    scene d7rachel116 with dissolve
    r "Quiet, mostly. I did some cleaning this morning and then just… rested. I’ve been feeling a bit drained lately."

    #scene d7rachel115 with dissolve
    scene d7rachel111 with dissolve
    l "Mom, you’ve been saying that for days. We barely leave the apartment anymore."

    scene d7rachel110 with dissolve
    mc "Do either of you feel like doing something this afternoon? We could go for a walk, grab a coffee, or just stay in if you prefer."

    scene d7rachel090 with dissolve
    r "I’d rather stay home and rest. I’m not in the mood to go out today. Maybe tomorrow."
    scene d7rachel112 with dissolve
    l "Ugh, you’re so boring, Mom. We finally have a free afternoon and all you want to do is sit on the sofa like an old lady."

    scene d7rachel115 with dissolve
    r "Lucy, I’m just tired."
    l "Ever since we got back from the trip you’ve been acting like you need a nap every two hours."

    scene d7rachel120 with dissolve
    mc "We’ll see. No pressure today if she wants to rest."
    r "Thank you. I just need a quiet afternoon."
    l "Boring…"


    scene d7rachel125 with dissolve
    r "I’m really tired… I think I’m going to go lie down for a while. You two can stay here."
    l "Yeah, go ahead, Mom. You look exhausted. Go sleep it off."

    scene d7rachel130 with dissolve
    r "You’re not going to complain that I’m being boring again?"
    l "Nah. You’re clearly dead on your feet. Better you rest than force yourself to stay up. I’ll keep [player_name] company for a while."
    #mc "She’s right. Go rest. We’ll be fine here."


    scene d7rachel135 with dissolve
    r "Alright… thank you. Don’t make too much noise, okay?"
    l "Yeah, yeah. Go sleep. We’ll talk quietly."

    # Rachel walks toward the bedroom.

    #mc "(watching her leave) She really does look tired lately."


    scene d7rachel140 with dissolve
    l "Finally… just the two of us. Mom is always around, it’s hard to get a moment alone with you."
    mc "Lucy… what are you doing?"


    scene d7rachel145 with dissolve
    l "Relax. I’m just getting comfortable."

    # She shifts in the chair. Her very short skirt rides up, and it becomes clear she isn’t wearing any panties.

    #l "Mmm… I’ve been thinking about this since I got here. Watching you, waiting for a chance."

    # She hooks her fingers under the hem of her short skirt and starts pulling it up higher, then slowly sliding it down her hips.

    scene d7rachel150 with dissolve
    l "Are you going to get naked too?"

    scene d7rachel154 with dissolve
    l "Or do you prefer watching me play with myself first?"

    # The short skirt comes off, leaving her completely bare from the waist down as she continues touching herself in front of him.

    $ renpy.movie_cutscene("images/lucy3.webm", loops=1, delay=None)

    scene d7rachel154 with dissolve
    l "Your move, [player_name]. Are you just going to stare… or are you going to do something about it?"

    menu lucy7_choice:
        "Accept Lucy's proposal":
            jump d7lucy# The scene continues with Diana and MC becoming intimate.

        "Reject her politely":
            scene d7rachel152 with dissolve
            mc "Lucy, stop. I appreciate the attention, but I’m with Rachel. I want to stay loyal to her."
            l " …You’re serious?"

            scene d7rachel153 with dissolve
            mc "Yes. I’m not going to do this behind her back."
            l "Huh. Fine, your loss—go running back to Rachel then, and I hope you get really lucky."

            jump d7rachel2
    return

label d7lucy:
    scene d7rachel155 with dissolve
    mc "Fine… you win."
    l "Mmm… look at that. You were pretending to be all loyal, but your cock is already this hard for me."

    mc "You’re not exactly making it easy to stay loyal."

    # She spreads her legs wider on the chair and starts fingering herself more deliberately, putting on a show for him.
    scene d7rachel160 with dissolve
    l "You like watching me play with myself, don’t you? Let me take care of this for you…"
    mc "Go ahead then."

    # She wraps her hand around his shaft and gives it a few slow, firm strokes.
    scene d7rachel170 with dissolve
    l "So thick… I’ve been wanting to feel this since I got here...mmmph"

    # She leans in and takes him into her mouth, starting with the head, then slowly pushing deeper.
    scene d7rachel165 with dissolve
    l "Mmm… gluck…"
    mc "Fuck… that’s it. Take it deeper."

    # She keeps going, taking more of him, her throat relaxing as she tries to deepthroat.
    scene d7rachel175 with dissolve
    l "gluck… gluck-gluck… mmmph"
    mc "You’re really trying to swallow all of it…"

    #l "gluck… gluck-gluck… mmmph"


    # She reaches up with one hand and squeezes her own breast while keeping her mouth full of him.
    scene d7rachel180 with dissolve
    l "gluck… gluck-gluck… mmmph"
    mc "You’re really choking yourself on it…"

    # She forces herself even deeper, eyes watering slightly as she struggles to take more of him, still groping her tit.

    scene d7rachel185 with dissolve
    l "Fuck… my throat is going to be sore after this."

    # She wipes her mouth with the back of her hand, still on her knees, looking up at him with clear hunger.
    scene d7rachel195 with dissolve
    l "Come on. Let’s move to the sofa. I want you properly."
    mc "You sure?"

    scene d7rachel190 with dissolve
    l "Don’t make me ask twice. Put it in. I want to feel that thick cock stretching me open."

    # MC pushes into her from behind in one firm thrust.

    scene d7rachel200 with dissolve
    l "Ahh—fuck yes! Just like that… fill me up!"
    mc "You’re so fucking tight…"

    # He starts thrusting steadily in doggy style.
    scene d7rachel205 with dissolve
    l "Harder… don’t hold back."
    mc "You were this wet just from teasing me earlier?"
    scene d7rachel210 with dissolve
    l "Listen to how wet I am… your cock is making such a filthy sound inside me."
    mc "I can hear it. You’re dripping all over me."

    #l "Because I want it. I want every fucking inch. Use me."

    #mc "Then take it. All of it."

    # After a while she shifts, turning onto her back and spreading her legs wide.

    #l "Come here… I want to look at you while you fuck me."

    #mc "You look even better like this."

    # MC moves into missionary and sinks back into her.
    scene d7rachel211 with dissolve
    l "Yes—right there… so deep… I can feel you all the way inside."
    mc "You feel incredible… so warm and wet."

    scene d7rachel212 with dissolve
    l "Don’t stop. Fuck me like you’ve been holding back for days. I want to feel it tomorrow."
    mc "Then I’ll make sure you feel it."

    scene d7rachel213 with dissolve
    l "You’re so hard… so thick… keep pounding this pussy. It’s all yours right now."
    mc "You’re taking me so well… look at how your body is reacting."

    scene d7rachel215 with dissolve
    l "Harder… deeper… make me take it. I love having your cock buried inside me like this."

    scene d7rachel216 with dissolve
    mc "Lucy… I’m close—"
    l "Me too—don’t pull out! Cum inside me—fill me up!"

    # Both of them reach the edge at the same moment.
    scene d7rachel220 with vpunch
    mc "Fuck—taking it all—"
    scene d7rachel220 with hpunch
    l "Ahh—yes! I can feel it—you’re cumming so deep inside me—!"

    # Their bodies tense together as they share the climax, MC pulsing inside her while she trembles underneath him.


    scene d7rachel221 with dissolve
    l "Mmm… so warm… I can feel every drop…"
    mc "That was… intense."


    # Diana slips down to her knees in front of MC. She wraps her fingers around his cock, still slick with their mixed fluids, and slowly strokes him.

    scene d7rachel230 with dissolve
    l "Look at this mess… you came so much inside me."

    # She leans in and drags her tongue along the shaft, tasting the remaining cum.

    #scene d7rachel240 with dissolve
    scene d7rachel231 with dissolve
    l "Mmm… still warm. I like the way we taste together."

    # She gives the head a few more lazy licks, cleaning him.
    scene d7rachel240 with dissolve
    mc "I should go check on Rachel. And I hope I still have enough energy left to satisfy her."
    l "Ambitious. Good luck with that."

    jump d7rachel2

    return

label d7rachel2:
    scene d7rachel305 with dissolve
    mc "(Thinking) {i}She’s completely naked… she must have gotten undressed before lying down. Her body looks so soft and calm like this.{/i}"

    # He sits carefully on the edge of the bed and gently touches her shoulder.
    scene d7rachel310 with dissolve
    mc "Rachel… hey."
    scene d7rachel315 with dissolve
    r "Mmm… [player_name]? You’re here…"
    mc "You look beautiful like this…"

    # He lets his hand rest lightly on her waist, trying to create a more seductive atmosphere.

    mc "Maybe we could… spend a little time together before the evening?"
    scene d7rachel317 with dissolve
    r "That’s sweet… but I’m really exhausted. My body feels heavy. I just want to keep sleeping a bit longer."
    mc "Are you sure? I could help you relax…"
    scene d7rachel318 with dissolve
    r "Not right now, okay? I appreciate it, but I’m too tired. Maybe later tonight… if I feel better."

    # She turns slightly, settling back into the pillow, already drifting off again.
    scene d7rachel319 with dissolve
    r "Just… let me rest a little more…"
    mc "(Thinking) {i} She’s really out of energy.{/i}"

    scene d7rachel320 with dissolve
    r "Maybe another day, okay…? I just don’t have the energy right now....zzz"
    mc "…Alright. Rest well."

    # He stands up and walks toward the door. Before leaving, he glances back at her naked body on the bed one last time.
    scene d7rachel325 with dissolve
    mc "(Thinking) {i} She looked so good lying there completely naked… it got me excited just seeing her like that. But this keeps happening. {/i}"
    scene d7rachel326 with dissolve
    mc "{i}Every time I try, she’s too tired. It feels like she never really wants to have sex with me anymore. {/i}"

    jump end
    return



############################################################ DAY 6 ##################################################

label decission:
    scene d6barcharla010 with dissolve
    r "[player_name]… can we talk? I’ve been thinking a lot lately."
    mc "Of course. What’s on your mind?"

    scene d6barcharla040 with dissolve
    r "I’m unsure about us. About everything. Lucy joined us so suddenly and… I feel like we’ve barely had time alone. I need to know how you really feel."

    scene d6barcharla070 with dissolve
    r "Do you truly love me? Do you want to stay with me? Or… is there someone else you’d rather be with?"

    # Rachel looks at him with anxious, hopeful eyes, waiting for his answer.
    scene d6choose_simple02 with dissolve
    pause 3.0
    menu relationship_choice:
        "I want to be with Crystal":
            scene black01
            mc "Rachel… I’ve fallen for Crystal. I want to explore things with her."
            jump crystal_end

        "I want to be with Claudia":
            scene black01
            mc "I care about you, Rachel… but my feelings for Claudia have grown stronger. I want to be with her."
            jump claudia_end

        "I want to be with Rachel":
            scene black01
            mc "Rachel… I love you. I want to be with you. You’re the one I choose."
            jump rachel_end

        "I want to be with Alina":
            scene black01
            mc "I’m sorry, Rachel. I’ve developed strong feelings for Alina. I want to be with her."
            jump alina_end

        "I want to be with Mabel":
            scene black01
            mc "I care about you, but Mabel… she’s the one I want to be with."
            jump mabel_end

    return

label rachel_end:

    scene rachel_selected with dissolve
    ga "You met many incredible women—each one special in her own way. They all wanted a place in your life, but in the end, you could only choose one. The others felt the weight of your decision, trying to hide their sadness. And now, one chapter closes while another begins."

    scene d6rachel_final010 with dissolve
    ga "Rachel is a loving, caring, and quiet woman. She possesses a beautiful body but rarely shows it in public, preferring privacy and emotional intimacy over bold displays. Although she doesn’t always express her feelings openly, she genuinely cares for you and wants a stable, meaningful relationship."

    scene d6rachel_final020 with dissolve
    ga "Sex is not her main focus like it is for the other women — what she truly values is tenderness, trust, and building something real with you."

    scene d6rachel_final030 with dissolve
    ga "However, Rachel’s life comes with its own challenges. Her daughter Lucy is always present.  and has made it very clear that she wants you for herself. Lucy competes constantly — flirting, teasing, and trying to pull your attention away."

    scene d6rachel_final050 with dissolve
    ga "This creates ongoing tension that Rachel struggles to manage, often leaving her feeling insecure and torn between her daughter and her love for you."

    scene d6rachel_final040 with dissolve
    ga "Can you handle the constant interference from Lucy? Can you set firm boundaries with her daughter while staying faithful and patient with Rachel? Rachel’s love requires the ability to navigate a complicated mother-daughter dynamic."

    jump d7rachel_end
    return

label claudia_end:

    scene claudia_selected with dissolve
    ga "You met many incredible women—each one special in her own way. They all wanted a place in your life, but in the end, you could only choose one. The others felt the weight of your decision, trying to hide their sadness. And now, one chapter closes while another begins."

    scene d6claudia020 with dissolve
    ga "Claudia is a force of nature — wild, unapologetic, and impossible to ignore."


    scene d5_beach_no2 with dissolve
    ga "A true nudist and exhibitionist at heart, she thrives on attention and pleasure."

    scene d6claudia050 with dissolve
    ga "Sex is not just something she enjoys; it’s part of who she is. Many nights you’d come home to find her waiting naked, already wet and ready."

    scene d6claudia060 with dissolve
    ga "She might tease strangers in front of you just to watch your reaction, then drag you to the nearest private corner to ride you senseless. Claudia is passionate, generous, and loyal in her own way."

    #scene wedding_claudia3 with dissolve
    #ga "She has even started talking about marriage — not in a traditional sense, but as a promise that you are her favorite person in the world."

    scene d6claudia070 with dissolve
    ga "She has no jealousy, no boundaries, and is more than happy to invite others into your bed if the mood strikes. With her, life would never be boring."

    scene d3clauride030 with dissolve
    ga "With Claudia, you’d never lack excitement. Her body, her confidence, and her insatiable appetite would keep you addicted for years. She truly loves you — in her own bold, chaotic, and very sexual way."

    scene d6claudia030 with dissolve
    ga "Can you keep up with her? Can you handle watching her flirt with others, even in front of you? Can you accept her when she flashes strangers? Claudia will never change… are you ready to live life at her speed?"

    jump d7claudia_end
    return

label alina_end:


    scene alina_selected with dissolve
    ga "You met many incredible women—each one special in her own way. They all wanted a place in your life, but in the end, you could only choose one. The others felt the weight of your decision, trying to hide their sadness. And now, one chapter closes while another begins."

    scene d6alina040 with dissolve
    ga "Alina is a quiet, gentle soul who loves with her entire heart. Once she falls for you, she becomes completely loyal and devoted. She has no interest in exploring sex with other people. She wants a real, intimate connection with just one person: you."


    scene d6alina010 with dissolve
    ga "With Alina, life would be peaceful and full of tenderness. She dreams of building something real with you — a stable relationship, perhaps marriage one day..."


    scene d5alina096 with dissolve
    "..and quiet nights where it’s just the two of you."

    scene d6alina020 with dissolve
    ga "But she will often feel insecure when other women are around, especially those who have more voluptuous bodies. Her jealousy is soft and quiet, never explosive, but it’s there — a constant need for reassurance that she is enough for you."

    scene d6alina030 with dissolve
    ga "Can you handle her insecurities? Can you accept that she will always be a little jealous? Alina’s love is pure and unwavering — but it requires patience, understanding, and gentle care."

    jump d7alina_end
    return

label crystal_end:

    scene crystal_selected with dissolve
    ga "You met many incredible women—each one special in her own way. They all wanted a place in your life, but in the end, you could only choose one. The others felt the weight of your decision, trying to hide their sadness. And now, one chapter closes while another begins."

    scene crystal_alone020 with dissolve
    ga "Crystal is pure passion, exhibitionism, and raw sexuality. She thrives on being desired, on pushing boundaries, and on living her pleasure without shame."

    scene crystal_alone060 with dissolve
    ga "But beneath that bold and seductive exterior lies a deeply caring, loving, and devoted woman who, once she falls for you, gives her heart completely."

    scene d4lock060 with dissolve
    ga "She will worship you with her body and soul, always eager to please and explore."

    scene d4lock050 with dissolve
    ga "With Crystal, life would never be boring. She will want you often, openly, and sometimes in risky places. She will love you fiercely and remain loyal. Her love is intense, passionate"

    scene crystal_alone070 with dissolve
    ga "However, Crystal carries a constant insecurity. As a futa, she lives with the fear of rejection — from society, from strangers, and most painfully, from the person she loves. She needs to feel wanted, not just sexually, but truly accepted for who she is."

    scene crystal_alone080 with dissolve
    ga "Can you handle her insecurities? Can you reassure her every time she feels different? Crystal’s love is beautiful and all-consuming — but it requires patience, understanding, and unwavering acceptance."

    jump d7crystal_end
    return

label mabel_end:

    scene mabel_selected with dissolve
    ga "You met many incredible women—each one special in her own way. They all wanted a place in your life, but in the end, you could only choose one. The others felt the weight of your decision, trying to hide their sadness. And now, one chapter closes while another begins."

    scene d6mabelfinal010 with dissolve
    ga "Mabel is a proud nudist and a shameless exhibitionist at heart. She loves gathering attention, feeling desired, and living without shame."

    scene d5_night082 with dissolve
    ga "Deep down, she desperately wants someone solid in her life — a partner who can accept her wild, sensual nature and still love her completely. "

    scene mabel_sx07 with dissolve
    ga "When Mabel loves, she loves fiercely and loyally. She won’t share you with anyone else… though she might make an exception for Sara."

    scene d5_night150 with dissolve
    ga "With Mabel, life would be exciting, sensual, and full of confidence. She will dance for you, strip for you, and make love to you openly and passionately."


    scene d6mabel_final010 with dissolve
    ga "Sara has seemed to accept that you and Mabel are together"

    scene sarashyleave033 with dissolve
    ga "But Sara is emotionally unstable. She often craves attention, gets jealous easily, and sometimes tries to pull you away for herself. This creates a constant, delicate tension — balancing Mabel’s bold exhibitionism with Sara’s needy and unpredictable behavior."

    scene d6mabelfinal020 with dissolve
    ga "Can you handle this complicated dynamic? Can you give Mabel the freedom and admiration she needs while gently managing Sara’s jealousy and instability? Mabel’s love is bold, generous, and deeply loyal — but it comes with its own beautiful chaos."

    jump d7mabel_end

    return

label end:
    scene black01
    pause 5.0
    centered "Thank you so much for playing Beachfront!
I really hope you enjoyed the story, the characters, and all the moments we shared together.
You can find me on {a=https://www.patreon.com/c/Madymor}Patreon{/a} — everyone is welcome, even if you join for free.
I’d love to hear your thoughts and feedback. Feel free to leave a comment or message me anytime.
Thank you again for playing.
See you in the next adventure!"
    $ renpy.movie_cutscene("/images/final.webm")
    scene d6final02
    pause 5.0
    #$ renpy.movie_cutscene("images/dance.webm", loops=1, delay=None)
    scene black01
    centered "The End"
    $ MainMenu(confirm=False)()
    return


################### DAY 6 #################################

label d6bar:
# Image 010

    scene black01
    centered "At night, you, Rachel, and Lucy go to the bar."

    scene d6bar010 with dissolve
    mc "You both look incredible. Rachel, that dress is a masterpiece on you... and Lucy, you look breathtaking. I'm easily the luckiest guy tonight."

    r "I wanted to make sure tonight felt special."

    l "Better get used to it! We're turning heads tonight"

    # Image 050
    scene d6bar050 with dissolve
    mc "Wow! The bar is completely full!"
    scene d6bar020 with dissolve
    l "My posts and streams really worked!"
    r "I can’t believe how many people came. Mabel must be so relieved."



    scene d6bar060 with dissolve      # Image 060
    mc "I see Sara working at the bar. I’m going to go say hi to her real quick."

    scene d6bar030 with dissolve
    r "Okay, we’ll find a good table."

    # Image 100

    scene d6bar100 with dissolve
    mc "Great job, Lucy. You really made this happen."
    l "Thanks! I’m going to keep taking pics and streaming the party live. The more people watch and pay to join, the more money we can raise for Mabel tonight."


    # Image 070
    # MC approaches the bar. Sara is wearing a very revealing minimal bikini maid costume.

    scene d6bar070 with dissolve
    mc "Sara, you look incredible in that outfit. Really suits you."
    sar "T-thank you… It was Lucy’s idea. I feel a bit exposed, but… I’m happy you like it."

    # Image 091

    scene d6bar091 with dissolve
    sar "The night is a huge success! So many people showed up… drinks are selling like crazy. Mabel is over the moon."
    mc "That’s fantastic. You’re doing great work."

    scene d6bar092_2 with dissolve
    sar "Thank you for coming… and for helping Mabel. It really means a lot."

    # Image 093
    scene d6bar093 with dissolve
    cryst "Hey, [player_name]! Look who’s working tonight~"

    # Image 094
    scene d6bar094 with dissolve
    cryst "What do you think? Does this uniform look good on me?"

    mc "You look great, Crystal. Very eye-catching."

    cryst "Good. That’s the idea. I’ll see you later, handsome."

    # Image 095
    # Crystal walks away toward Rachel and Lucy’s table, swaying her hips and ass noticeably.
    scene d6bar095_inc with dissolve
    mc "Damn… Crystal’s ass looks so good in that tiny outfit. The way it sways when she moves is driving me crazy."

    # Image 102
    scene d6bar102 with dissolve
    w "Hi, [player_name]. I came, just like you asked."

    sar "Hi! You look really pretty."


    # Image 106
    scene d6bar106 with dissolve
    w "I’m here to help. You said you needed people to make the bar look full tonight, so… here I am."
    mc "Thanks Alina"

    # Image 104
    scene d6bar104 with dissolve
    w "You look good tonight. I’m happy I get to spend some time with you."

    # Image 108
    scene d6bar108 with dissolve
    l"Hey, [player_name]! Can I borrow her for a moment? I want to take some cool pics of her for the stream."

    # Image 112
    scene d6bar112 with dissolve
    l "Come on! You look amazing in that dress. Let’s get some shots with the lights and the crowd behind you."
    w "Sure, sounds fun."

    # Image 114
    scene d6bar114 with dissolve
    w "I’ll go with her for a bit… but I’ll come find you later, okay?"
    mc "Sounds good. Have fun."

    scene d6mabel_present010 with dissolve
    mab "Excuse me, everyone! Can I have your attention for just a moment?"

    # The crowd quiets down, turning toward the stage.
    scene d6mabel_present032 with dissolve
    mab "First of all, thank you… thank you so much for coming tonight. I’ve never seen the Show Bar this full and this alive. It really means everything to me."

    scene d6mabel_present050 with dissolve
    mab "I also want to give a very special thanks to the people who helped make tonight possible… especially [player_name]. Without him, none of this would have happened."

    stop music fadeout 2.0

    # The crowd applauds. Mabel smiles softly.
    scene d6mabel_present020 with dissolve
    mab "And now, the moment you’ve all been waiting for… please welcome our star performer — the incredible Claudia!"

    play sound "Applause.mp3"

    play music beach loop

    # The lights shift as Claudia steps onto the stage in a striking outfit, ready for her pole dance.
    scene d6claudia_dance07_2 with dissolve
    c "Are you ready to have some fun tonight?"


    scene d6claudia_dance020 with dissolve
    l "Oh my god, Mom… Claudia is so freaking hot up there! Look at how she moves around that pole. She’s killing it!"

    scene d6claudia_dance041 with dissolve
    r "She really is… I have to admit, for a woman her size, she moves incredibly well."

    scene d6bar200 with dissolve
    l "Exactly! She owns that stage. I love how bold she is."
    r "She definitely knows how to put on a show."

    scene d6claudia_dance030 with dissolve
    c "Watch this big juicy ass bounce for you... You want to slap it, don’t you?"

    scene d6barnew005
    sar "She’s… so beautiful. The way her tits bounce when she spins… and that ass… I can’t stop staring."

    scene d6barnew020
    cryst "Yeah… she really knows how to move."

    scene d6barnew010 with dissolve
    cryst "Fuck… I’m getting hard just watching her."

    scene d6barnew040 with dissolve
    cryst "I… I can’t help it. Watching her dance like that just… gets me so hard. This is so embarrassing."
    sar "It’s okay… I don’t mind."


    scene d6claudia_dance045 with dissolve
    cryst "Yeah… she’s got that effect on people."

    scene d6claudia_dance050 with dissolve
    sar "I’ve never seen anyone dance like that…"


    scene d6claudia_dance060 with dissolve
    sar "It’s like she’s owning everyone in the room."

    scene d6claudia_dance075 with dissolve
    cryst "God… look at her move."
    scene d6claudia_dance080 with dissolve
    cryst "That body is fucking sinful."
    scene d6claudia_dance091 with dissolve
    c "There they are… my big, heavy tits just for you."
    scene d6claudia_dance095 with dissolve
    c "You’ve been staring at them all night…"
    scene d6claudia_dance099 with dissolve
    c"...Now they’re yours to enjoy."
    scene d6claudia_dance101 with dissolve
    c "Look at me… open and ready... You like what you see?"
    scene d6claudia_dance100 with dissolve
    c "That’s all for tonight, my loves…"


    scene d6mabel_present032 with dissolve
    mab "Let's hear it for Claudia, everyone—give her a huge round of applause!"
    play sound "Applause.mp3"
    stop music fadeout 2.0

    play music musica5 loop
    # The music intensifies as the crowd cheers loudly.
    return



label morningd6old:
    # Lucy enters completely naked, phone in hand, a playful and seductive smile on her face. She raises the phone and snaps a quick photo of MC lying naked on the bed.

    scene d6_luc030 with dissolve
    l "Good morning, handsome… Don’t move. You look way too good right now."
    mc "Lucy—? What are you doing? I thought you were taking a shower. You should—"

    scene d6_luc035 with dissolve
    l "Shhh… I lied. I wanted to catch you like this. Alone and naked..."
    mc "Lucy, we can’t… Rachel might walk in any second..."

    scene d6_luc045 with dissolve
    l "Then we’ll have to be fast and quiet, won’t we? Besides… I’ve been dying to play with you all week."

    scene d6_luc060 with dissolve
    l "Look at this big, hard cock… all mine right now. Smile for the camera, baby. These pics are just for my private collection."

    menu lucy_choice:
        "Let Lucy continue":
            mc " …Fuck it. You’re impossible. Just… be quiet."
            scene d6_luc055 with dissolve
            l "Good boy. Now lie back and let me take care of you."

            scene d6luc160 with dissolve
            l "Mmm… so thick… I love how you taste in the morning…"
            mc "Rachel… why are you recording everything? The phone—"

            scene d6_luc081 with dissolve
            l "All the girls my age love having naughty pics and videos of their boyfriend’s cock. I want to look at it when I’m alone… touch myself thinking about you."

            # She dives back down, taking him deeper into her warm, wet mouth.
            scene d6luc120 with dissolve
            l "mmmph… slurp… gluck…"

            scene d6luc130 with dissolve
            #l "Shhh… be quiet, handsome. Mom can’t hear you moaning like that… just let me suck you off."

            mc "Fuck—Lucy—I’m gonna—"
            scene d6luc145 with dissolve
            l "slurp-slurp-gluck… mmmph…"


            scene d6luc180 with dissolve
            l "Mmm—give it to me… fill my mouth…"

            # MC tenses, hips jerking. He comes hard—thick pulses flooding her mouth. Rachel moans softly, swallowing every drop, eyes locked on his the whole time.

            l "Mmm… delicious. My favorite morning protein."

            # She stands up gracefully, still completely naked, and leans down to kiss him once—deep and slow.

            l "Gotta go before Mom comes back. Don’t miss me too much… I’ll be thinking about your cock all day."


        "Ask Lucy to stop":
            mc "Lucy… we really shouldn’t. Not right now. Rachel’s just down the hall."
            scene d6_luc_leave with dissolve
            l "Aww… you’re no fun. But fine… I’ll behave. For now."

            scene d6_luc_leave02 with dissolve
            #l "But you owe me later. A lot."

            # She stands up, still naked, and walks toward the bathroom with a sway in her hips.

            l "Don’t forget… I still have that shower to take. You’re welcome to join if you change your mind."


    return



label beachd6:
    scene black01
    centered "Later in the morning, you, Rachel, and Lucy go to the beach together."

    scene d6beach015 with dissolve
    r "Okay… I’ve been thinking about this all morning."
    l "Thinking about what, Mom?"

    scene d6beach020_2 with dissolve
    r "My new style. I’m… trying something different today. I hope you both like it."

    scene d6beach030_2 with dissolve
    r "Well…? No more hiding. This is me now."
    mc "Rachel… wow. You look stunning. Really confident. I love it."

    scene d6beach030_3 with dissolve
    l "Mom! Oh my god—you look {b}amazing{/b}!"



    #scene d6beach025 with dissolve
    #r "You do? I was so nervous… but seeing you both react like that… it feels good."

    #scene d6beach026 with dissolve
    #l "If Mom’s going topless, then so am I!"

    scene d6beach027 with dissolve
    # Lucy unties her bikini top and tosses it aside, small breasts bare in the sun.
    #scene d6beach030 with dissolve
    l "Matching vibes! Beach twins—topless edition!"
    r "You’re impossible… but okay."

    # Both women lie down on their towels side by side, topless, soaking up the sun.
    scene d6beach035 with dissolve
    l "This is the best. No more tan lines, no more stress. Perfect."
    r "I think I’m finally starting to believe that."
    mc "You two look happy. I’m gonna go for a little walk along the shore—give you some space to relax. I’ll be back in a bit."

    scene d6beach040 with dissolve
    l "Don’t get lost… or find any more naked ladies..."
    r "Be safe. And come back soon—we might need sunscreen help later."
    mc "Wouldn’t miss it."

    return

label mabeld6:

    scene seaside
    mc "(thinking) {i}Let's see if I can find Mabel around here.{/i}"
    scene d6mabel010 with dissolve
    mc "Damn… Mabel’s lying there completely naked, looking like she owns the whole beach… and Sara’s right beside her. This morning just got a lot more interesting."
    scene d6mabel020 with dissolve
    mc "Mabel? Sara?"
    mab "[player_name]! What a lovely surprise. Come join us, handsome."
    sar "H-hi, [player_name]… nice to see you again."

    scene d6mabel022 with dissolve
    mc "Hey… didn’t expect to find you two here. You look… comfortable, Mabel."
    mab "Oh, I’m very comfortable. No tan lines, just sun on every inch. I love it."

    scene d6mabel029 with dissolve
    sar "Don’t mind mom, she loves sunbathing like this, and honestly… it feels totally normal now."

    scene d6mabel034 with dissolve
    mab "You used to be so shy about me being, well, 'gifted.' If you're feeling uncomfortable, feel free to take your game a little further down the beach. I won't be offended, honestly!"
    sar "No, Mom, I’m okay. I’ve… grown out of that, I think."

    scene d6mabel036 with dissolve
    mab "It’s such a relief that she’s over her shy phase."
    sar "Mom, stop. [player_name] knows I’ve gotten over it. It’s not a big deal anymore."

    scene d6mabel038_1 with dissolve
    mab "I’m curious... how exactly is [player_name] in the loop on your 'progress'?"

    scene d6mabel038_2 with dissolve
    sar "Actually, I spent yesterday baring it all with Lucy and Claudia. I wasn’t shy for a second—in fact, I totally loved it."

    scene d6mabel038_3 with dissolve
    sar "So, if you don’t mind, I’m ditching my top right now."

    scene d6mabel040 with dissolve
    mab "Oh, honey, you look wonderful! I knew you'd get there eventually."
    sar "Well? I hope you're not disappointed, [player_name]. I was kind of counting on you liking the view."
    mc "Honestly, Sara? You look incredible."


    scene d6mabel042 with dissolve
    mab "Oh, look at you! My girl is finally all grown up and free. Come here, honey. Give your mom a hug!"
    sar "Heh, alright, alright... don't get all sappy on me."

    scene d6mabel044 with dissolve
    mab "I mean it, Sara. I’m just so incredibly proud of you. Seeing you this comfortable... it’s like a weight has been lifted off both of us."

    scene d6mabel046 with dissolve
    mab "And [player_name]...I honestly don’t know what kind of magic you worked on her yesterday, but thank you."
    mc "I just helped her realize she had nothing to hide, Mabel. She did the rest."

    scene d6mabel048 with dissolve
    sar "Careful, [player_name]. Now that I've started, I might just decide to go even bolder."
    mab "Goodness! Even bolder? I didn't think that was possible!"

    scene d6mabel050 with dissolve
    #sar "Believe it, Mom. I’m just getting started."
    sar "You know, Mom... wearing this tiny piece of fabric feels almost... dishonest now. Like I'm still hiding a part of the 'new me'."
    mab "Well, there's no room for secrets on this beach, honey. If you're ready to let it go, I'm right here with you."



    scene d6mabel052 with dissolve
    sar "What do you think, [player_name]? Should I take the final plunge? Or is the suspense killing you?"
    mc "I think you’ve already made up your mind, Sara. But yeah... I’m definitely watching."

    scene d6mabel054 with dissolve
    sar "There. Total honesty. I have to admit, Mom... the breeze feels a lot better when there's nothing in the way."
    mab "I told you! It’s liberating, isn’t it? You look absolutely stunning, Sara. Every bit a woman."

    scene d6mabel056 with dissolve
    sar "See anything you like, [player_name]? Because I’m not planning on putting these back on anytime soon."
    mab "I think he’s speechless, honey. And can you blame him? Seeing both of us like this... it’s quite the view for one man."

    scene d6mabel058 with dissolve
    mab "You’ve grown so bold, Sara. I think I like this version of you much better. So... confident. So... exposed."
    sar "I learned from the best, Mom. Maybe we should show [player_name] exactly how much I've 'improved' since yesterday..."

    scene d6mabel058_2 with dissolve ##FALTA mabel miran a mc
    mab "Actually, Sara... I’m quite curious myself. Why don't you show me exactly what you 'learned' yesterday while [player_name] watches?"

    scene d6mabel074 with dissolve
    sar "So, what’s it going to be? Do you want to stay and see exactly what Mom and I can do together?"
    mc "I definitely want to see that. I’m not going anywhere."
    mab "Good choice. I was hoping you’d say that."


    scene d6mabel078 with dissolve
    sar "They’re so heavy… and warm… I can’t believe I’m doing this…"
    mab "You’re doing perfectly, baby girl. Squeeze a little harder… yes, just like that…"


    scene d6mabel079 with dissolve
    mab "Look at us… sweet little Sara playing with my big tits right in front of you. Enjoying the show?"
    sar "Does it make you hard seeing me hold her like this?"
    mc "Yeah… I’m definitely getting hard watching you two like this. You’re both so fucking gorgeous."


    scene d6mabel076 with dissolve
    sar "I used to be so jealous of… of how big and perfect your tits always were. "

    scene d6mabel060 with dissolve
    sar "But now… now I just want to play with your tits. They’re so full… so warm…"
    mab "Then play, baby girl. Squeeze them, feel how heavy they are. If you want… go ahead and lick my tits."

    scene d6mabel062 with dissolve
    sar " Mmm… they taste like sun and salt… so good…"
    mab "Fuck yes… just like that, sweetheart. Suck it harder—pull it into your hot little mouth. God, you’re making me so wet already…"

    scene d6mabel064 with dissolve
    sar "Mmmph… your nipple’s so hard between my lips…"
    mab "Keep going… bite it a little… yes—fuck, you’re a natural little tit-lover, aren’t you?"

    scene d6mabel066 with dissolve
    sar "I can’t just lick anymore—I need to kiss you. Please…"
    mab "Oh baby… I’ve wanted your mouth on mine since you first touched me. Kiss me..."

    scene d6mabel068 with dissolve
    sar "Mmmph… you taste so fucking good…"
    mab "Tongue deeper, little slut… let me taste how much you want me…"

    scene d6mabel080 with dissolve
    mab "You’ve turned into such a needy little thing, haven't you?"
    sar "Fuck… I can smell how turned on you are mom…"

    scene d6mabel082 with dissolve
    sar "[player_name]… do you want to join us?"
    mab "Come on, handsome. Don’t make us beg. Get those clothes off and play with us."


    menu:
        "Accept the invitation.":
            jump accept_spectacle

        "Politely decline and leave.":
            jump decline_and_leave

    return

label accept_spectacle:
    mc "You two are very convincing. Alright, I’m in."

    scene d6mabel086 with dissolve
    sar "We’re really going to share him?"
    mab "Oh yes, sweetie. We’re going to share him very well."

    #sar "I like that plan."

    scene d6mabel094 with dissolve
    mab "Look at him… already hard just from watching us. I want those tits of mine wrapped around that cock."
    sar "I… I want to use my mouth on him. I want to taste him."


    scene d6mabel096 with dissolve
    mab "Mmm, good girl. You suck him nice and sloppy, and I’ll milk him with my fat tits. We’ll make him explode all over us."
    sar "I want to feel him throb in my mouth… and I want to share his cum with you mom"

    mab "That’s my dirty girl. Let’s go get him. I want to see your pretty lips stretched around his cock while I titfuck him."


    scene d6mabel110 with dissolve
    sar "It’s so warm… and hard already. Can I… taste you?"
    mab "Go on, baby girl. Show him how much you’ve been wanting this cock."


    scene d6mabel114 with dissolve
    sar  "Mmm… you taste so good…"
    mc "Fuck… Saram, your mouth is so eager and warm… this is dangerous."


    scene d6mabel116 with dissolve
    mab "That’s it, Sara… nice and slow. Make him throb for us. Look how hard he is in your little mouth."


    scene d6mabel120 with dissolve
    sar "Do you like my mouth? I want to make you feel really good…"
    mab "My turn, handsome. Let me squeeze this thick cock between my tits."


    scene d6mabel130 with dissolve
    #mab "Feel how soft and warm they are? I love milking cocks with my big tits… especially yours."
    mc "Jesus… the way your tits are smothering me… it’s too fucking good. I’m not gonna last long like this."
    sar "You look so hot like that, Mom… his cock disappearing between your tits…"
    mab "He’s getting close already. I can feel him throbbing between my boobs. You want to come all over us, don’t you, [player_name]?"

    scene d6mabel135 with dissolve
    #sar "I want it first… please come on me."
    #mab "That’s right, baby. Let Sara have the first load. She’s been such a good girl today."

    sar "I’m ready… I want to feel it on my face and tits."
    mab "Look at her, [player_name]. She’s practically begging for your cum. She’s so cute when she’s desperate. Give it to her."

    scene d6mabel140 with dissolve
    sar "Come on me… please… I want to be your dirty girl."
    mab "That’s it… paint her. Make her messy."

    # MC groans and starts to climax. Thick ropes shoot across Sara’s face and small breasts.
    scene d6mabel142 with dissolve
    sar "Oh my god… there’s so much… it’s all over my face…"
    mab "Now it’s my turn. Give me the rest, [player_name]."

    scene d6mabel144 with dissolve
    sar "It’s dripping down my chin… onto my tits… I love it…"
    mab "Mmm, so hot and sticky"

    scene d6mabel150 with dissolve
    mab "Fuck… it’s so warm… so much…"
    sar "Look at her udders… they’re perfect for this."

    scene d6mabel151 with dissolve #o d6mabel152 d6mabel153
    sar "You came so hard for us…"
    mab "We look so good covered in you…"


    scene d6mabel167 with dissolve #o d6mabel154
    mab "Come here, baby girl… let me kiss you."

    #mab "(moaning softly as she tastes) Mmm… he tastes so good on you."

    sar "Oh… mom…"

    # Sara kisses Mabel deeply, their tongues sliding together, sharing MC’s release between them.


    scene d6mabel166 with dissolve
    sar "I can taste him on your tongue… it’s so dirty… I love it."

    mab "You look so pretty covered in his cum. Let me get every drop."

    # Mabel continues licking Sara’s face clean — slow, sensual strokes of her tongue across her cheeks, lips, and jaw.

    scene d6mabel169 with dissolve
    sar "Your tongue feels so good… don’t stop…"

    mab "I’m not stopping until you’re clean, sweetheart. And then you can do the same to me."

    # Sara leans in and starts licking Mabel’s face in return — eagerly cleaning her cheeks and lips, occasionally kissing her deeply.

    scene d6mabel170 with dissolve
    mc "I have to head back to the apartment now, but I’ll see you both tonight at the bar. It’s going to be a big night."
    mab "We’ll be there."
    sar "I already have my outfit ready… I can’t wait to see you tonight."


    return

label decline_and_leave:

    mc "I think... I think this is where I should head out. You two clearly have a lot to catch up on, and I don't want to overstay my welcome."

    scene d6mabel090 with dissolve
    sar "Oh? Leaving so soon? And right when things were getting interesting..."
    mab "We'll miss the audience, but we'll certainly find a way to entertain ourselves. See you later, [player_name]."


    scene d6mabel088 with dissolve
    mab "Don’t stop, baby… keep playing with my big tits. Squeeze them harder, I love feeling your hands on me."
    sar "I’m going to have so much fun with these huge fucking tits… I want to bury my face between them and suck until you’re soaking wet for me."

    return


label d6beach2:
    scene seaside
    mc "{i}I'd better get back to Rachel and Lucy.{/i}"


    scene d6beach_return010 with dissolve
    mc "Hey, I’m back."


    scene d6beach_return020 with dissolve
    r "There you are. You took quite a while. Everything okay?"
    l "Yeah… you were gone for a long time. What were you doing?"
    mc "I ran into Mabel and Sara down the beach. We started talking and I lost track of time. Sorry about that."

    scene d6beach_return030 with dissolve
    r "Oh, that makes sense. I hope they’re doing well"

    scene d6beach_return040 with dissolve
    l "Just talking, huh? You look a little too… satisfied for someone who was only chatting."



    scene d6beach145 with dissolve
    r "It’s getting late. We should head back to the apartment."
    l "Yeah, let’s go home. It’s been such a great day!"
    mc "Agreed. Ready when you are."


    scene d6beach125 with dissolve
    l "Seriously, today was amazing!"
    r "It really was a wonderful day."

    scene d6beach135 with dissolve
    l "And I’m so happy I finally got to see you topless, Mom. You looked seriously hot."

    scene d6beach130 with dissolve
    r "Lucy… you’re impossible."


    scene d6beach140 with dissolve
    l "So [player_name]… don’t you like Mom’s tits? Be honest, they look pretty great, right?"
    r "Lucy! Stop that. You don’t have to answer her, [player_name]. Let’s just go home."
    mc "Yeah… I do like seeing you topless, Rachel. You look beautiful like this."

    scene d6beach120 with dissolve
    l "Ohhh? So you like Mom’s tits, huh? Would you like to see me touching them too?"
    r "Lucy! [player_name]..."

    menu mc_reaction:
        "Say yes":
            mc "…Yeah. I wouldn’t mind seeing that at all."


            scene d6beach200 with dissolve
            r "[player_name]…! You actually said that out loud…"
            l "Then… you have to let me touch them, Mom. Just for a second. Please?"


            scene d6beach205 with dissolve
            l "They’re so full and soft… I love how they feel in my hand."
            r "Oh… that feels… surprisingly good…"

            scene d6beach210 with dissolve
            l "Mmm… feels nice too…"

            scene d6beach215 with dissolve
            r "This is… much more exciting than I expected."
            l "Same… I can’t stop touching you, mom"


            scene d6beach220 with dissolve
            mc "Look at that…"

            scene d6beach225 with dissolve
            mc "both of your nipples are so hard right now. You two are really getting into this."



            scene d6beach230 with dissolve
            l "[player_name]… do you like what you see? Me touching mom like this?"
            mc "Yeah… I do. I like it a lot."
            r "I… I can’t believe I’m doing this."

            # Next scene: Sara moves behind Rachel, pressing her body against her back. Her hands slide up to gently caress Rachel’s bare breasts.


            scene d6beach240 with dissolve
            l "You feel so good… so soft and warm…"
            r "Lucy... it does feel nice… but I shouldn’t…"

            # Next scene:
            scene d6beach250 with dissolve
            r "Wait… we should stop. This is getting too far."
            l "It’s a pity… I was really enjoying it. And I think [player_name] was too."
            mc " …I was."

            # Next scene:
            scene d6beach255 with dissolve
            r "It’s time to go back to the apartment. We’ve been here long enough."
            l "Yeah, let’s head back. We need to get ready for the party at Mabel's tonight."
            mc "Before heading home, I need to stop by the ice cream shop."
            return

        "Say no":
            mc "Let’s not go there, Lucy. That’s a bit too much."

            scene d6beach255 with dissolve
            r "Ok, it’s time to go back to the apartment. We’ve been here long enough."
            l "Yeah, let’s head back. We need to get ready for the party at Mabel's tonight."
            mc "Before heading home, I need to stop by the ice cream shop."

    return








label morningd6:
    play music musica5 loop
    scene d6_luc005 with dissolve
    r "Morning, handsome. I’m going to take a shower… won’t be long."
    mc "Mmm… okay. Enjoy."


    scene d6_luc030 with dissolve
    l "Morning, sleepyhead…"
    mc "Lucy! What the hell? You’re naked and your mom’s in the shower, get out!"

    scene d6_luc035 with dissolve
    l "Shhh… relax. Mom’s busy with her hair routine. She won’t hear a thing."

    scene d6_luc045 with dissolve
    l "Smile for the camera..."
    mc "Put the phone down! "

    scene d6_luc055 with dissolve
    l "Look at you… already getting hard just from me being here. I love how easy you are."
    mc "Stop! Lucy, this is insane. Delete those pics right now and leave or..."

    scene d6_luc081 with dissolve
    l "Or what? You’ll tell Mom? And show her the pics I already have of you staring at naked Claudia and Sara yesterday? The ones where you’re clearly enjoying the view?"
    mc "You… you said those were private!"
    l "Oh, they do. For now. But I keep thinking… what if Mom saw them?"

    scene d6_luc065 with dissolve
    mc "You wouldn’t."
    l "I might… unless you let me have a little fun right now. Let me suck you off while the shower’s running."
    mc "This is insane. You’re blackmailing me with..."

    scene d6_luc080 with dissolve
    l "Not blackmail… just motivation. You either let me swallow you right here, right now… or I “accidentally” leave my phone unlocked when Mom comes back. Your choice, [player_name]."

    # She strokes him slowly, thumb circling the head, eyes locked on his.
    scene d6_luc_devil with dissolve
    l "Tick-tock… shower’s loud, but not that loud. So… are you gonna be a good boy and let me have my morning treat… or should I go show Mom what her man’s been up to?"

    menu lucy_blackmail:
        "Accept Lucy’s offer (let her continue)":
            mc "…Fine. Do it. But make it quick and quiet."

            scene d6_luc070 with dissolve
            l "Good boy. Now lie back… and let your naughty little stepdaughter take care of you."

            jump lucy_continue

        "Refuse her, even with the risk":
            mc "No. Delete those pictures, Lucy. Right now. I’m not playing this game."

            scene d6_luc_surprise with dissolve
            l "You sure? Mom’s gonna be *so* disappointed when she sees what her boyfriend’s been doing behind her back…"

            mc "Then she’ll see. But I’m not letting you blackmail me. Delete them—or don’t. Your call."
            scene d6_luc_leave with dissolve
            l "…You’re braver than I thought. Fine. I’ll delete them. For now."

            # She opens her phone, taps a few times, shows him the “deleted” confirmation.
            scene d6_luc_leave02 with dissolve
            l "But don’t think this is over. I still have backups. See you at breakfast, [player_name]."

            # She slips out, leaving MC alone, heart pounding.

    return

label lucy_continue:
    # Lucy continues—mouth working him deep, wet sounds muffled, eyes locked on his.

    scene d6luc160 with dissolve
    l "Mmm… so thick… I love how you taste in the morning…"
    mc "Lucy… why are you recording everything? The phone—"

    scene d6_luc081 with dissolve
    l "All the girls my age love having naughty pics and videos of their boyfriend’s cock. I want to look at it when I’m alone… touch myself thinking about you."

            # She dives back down, taking him deeper into her warm, wet mouth.
    scene d6luc120 with dissolve
    l "mmmph… slurp… gluck…"

    scene d6luc130 with dissolve
    mc "Fuck… Lucy…"


    scene d6luc140 with dissolve
    l "slurp-slurp-gluck… mmmph…"



    scene d6luc152 with dissolve
    l "mmm… slurp… gluck…"


    scene d6luc155 with dissolve


    # She speeds up, taking him to the back of her throat, gagging softly but not stopping.
    mc "Fuck...Lucy...I’m gonna..."

    scene d6luc156 with dissolve
    l "gluck-gluck… mmmph…"



    scene d6luc156_cum with dissolve
    mc "Aaahhhhh"

    # MC tenses. He comes hard—thick pulses filling her mouth. Lucy moans, swallowing eagerly.

    scene d6luc192 with dissolve
    l "Mmm… breakfast of champions."

    # She quickly wipes her mouth, kisses his cheek, and slips out.

    scene d6_luc_leave_cum with dissolve
    l "See you at breakfast, [player_name]. Mom’ll never know… unless you want her to~"


    return


label d6ice:

    scene d6ice010 with dissolve
    mc "(thinking) {i}There she is… Alina and Crystal attending her. Perfect.{/i}"

    scene d6ice020 with dissolve
    cryst "Hi, [player_name]. Good to see you again."
    w "[player_name]! You came. I was waiting for you."

    scene d6ice030 with dissolve
    w "Come sit with me. We can talk here."
    cryst "Welcome back! What can I get for you today?"
    mc "Thanks. I’m good, actually. I don’t need anything to eat right now."

    scene d6ice040 with dissolve
    cryst "Are you sure? If you want…"

    scene d6ice045 with dissolve
    cryst "If you want… anything later, just let me know. I can be very accommodating."

    # Crystal turns around to "organize" something behind the counter. She discreetly lifts the back of her short uniform skirt for a second, revealing her bare ass and no panties underneath, then quickly lowers it so only MC sees.
    scene d6ice050 with dissolve
    cryst "See? Just in case you get hungry later."

    scene d6ice_sad with dissolve
    w "Is it really necessary for you to look at every single girl when you're with me?... Never mind, just forget it."

    scene d6ice060 with dissolve
    w "So… what did you want to talk about?"
    mc "Alina, I wanted to talk to you because I need your help with something important. A friend of mine, Mabel, owns the Show Bar. She’s in real trouble — she has to pay a big bill in two days or she might lose the place."


    scene d6ice065 with dissolve
    w "That’s awful. What can I do to help?"
    mc "I’m trying to make tonight a huge success for her. Lucy is going to promote the party on social media and stream it live so more people will come and pay to join online."

    scene d6ice070 with dissolve
    w "I see… you want to fill the bar and get people to support her."
    mc "Exactly. The more people who show up tonight, the better chance she has to save the bar."

    w "Then count me in. I’ll be there tonight. I’ll help make the place look full."
    mc "Thank you, Alina. That means a lot."

    w "No problem. I’ll do what I can to help."


    # Image 75
    scene d6ice075 with dissolve
    cryst "Here’s your ice cream, Alina. Extra sprinkles, just the way you like it."

    w "Thank you, Crystal. It looks really good."

    cryst "And what about you, [player_name]? Still not hungry?"

    # Image 80
    scene d6ice070 with dissolve
    mc "Actually, yes. I want you to sit with us, Crystal. I need to talk to both of you."

    cryst "Oh? Alright, I’ll sit."

    # Image 84
    scene d6ice084 with dissolve
    w "…Sure."

    cryst "Perfect. Now we’re all together."

    # Image 86
    scene d6ice086 with dissolve
    w "Yeah…"

    cryst "So, what’s this about?"

    # Image 88
    # Alina and Crystal glance at each other, both trying to act natural.
    scene d6ice086 with dissolve
    w "Go ahead, [player_name]."

    cryst "We’re listening."

    # Image 105
    # Both women sit side by side in front of MC.
    scene d6ice105 with dissolve
    w " …"

    cryst "What’s on your mind?"

    # Image 110
    scene d6ice110 with dissolve
    mc "I need your help. A friend of mine, Mabel, owns the Show Bar. She’s about to lose the place if she can’t pay a big bill in two days. I want to make tonight a huge success so she can save it. Lucy is going to promote the party online and stream it live."

    cryst "I know that bar well. Poor Mabel… count me in. I’ll help however I can."

    # Image 140
    scene d6ice140 with dissolve
    cryst "I can work as a waitress tonight. That’s what I do best anyway — keeping the energy high and the customers happy."

    # Image 142
    scene d6ice142 with dissolve
    mc "You’ll be a very sexy waitress, Crystal. The place is going to look amazing with you there."
    cryst "Stop it… but thank you. I’ll make sure to wear something cute and eye-catching."

    # Image 115
    scene d6ice115 with dissolve
    w "Well… I guess we’ll meet again at the bar tonight."

    cryst "Yes, we will."

    # Image 120
    scene d6ice120 with dissolve
    cryst "You’re very pretty, Alina. I think we’re going to become good friends."

    w "…"

    # Image 125
    scene d6ice125 with dissolve
    w "[player_name], I don’t understand Crystal… I’m not interested in women."

    # Image 132
    scene d6ice132 with dissolve
    mc "Alina… Crystal is not exactly a woman. She’s a futa."

    # Image 125 again
    scene d6ice125 with dissolve
    w " …What?"

    # Image 136
    scene d6ice136 with dissolve

    menu crystal_choice:
        "Ask Crystal to show Alina in the bathroom":
            mc "Crystal… why don’t you show her in the bathroom? So she can see for herself."
            scene d6ice144 with dissolve
            cryst "Of course. Come with me, Alina. I’ll show you everything."

            jump d6toilet

        "Leave and see them at the bar tonight":
            mc "We can talk more later. I’ll see you both at the bar tonight."
            scene d6ice110 with dissolve
            cryst "We’ll be waiting for you."
            w "See you tonight."

    return

label d6toilet:
    # Image 1
    scene d6toilet010 with dissolve
    cryst "Alina… you said you’re not into women. But I’m not exactly a woman. Would you like to see what I really am?"
    w "I… I’ve never seen a futa before. I’m curious… but I’m also really nervous."
    cryst "That’s okay. I’ll show you slowly. No pressure."


    scene d6toilet020 with dissolve    # Image 2
    cryst "[player_name], you don’t mind if I show her, right?"

    mc "Go ahead. I think she wants to see."

    w "I… yes. I want to see."

    # Image 3
    # Crystal slowly removes her uniform, revealing her large breasts, soft belly, wide hips, and her thick, semi-hard cock.
    scene d6toilet030 with dissolve
    cryst "See? I’m a girl… with something extra. What do you think?"

    w "Oh my god… it’s so big… and it’s… really there. I didn’t expect it to look so… pretty."

    # Image 4
    # Alina slowly drops to her knees in front of Crystal, eyes fixed on her cock.
    scene d6toilet040 with dissolve
    w "It’s even bigger up close… I can see it twitching."
    cryst "You can look as much as you want, sweetie. Touch it if you’d like."

    # Image 5
    scene d6toilet050 with dissolve
    w "Can I… touch it? Just a little?"
    cryst "Of course you can. Go ahead, beautiful. It’s all yours to explore."

    # Alina reaches out with trembling fingers and gently wraps her hand around Crystal’s cock.
    scene d6toilet050 with dissolve
    w "It’s so warm…"

    # Image 55
    scene d6toilet055 with dissolve
    cryst "Do you like it, Alina? Because I’m really liking the way you’re touching me. You can feel how hard I’m getting, right?"

    w "I… yes. It’s so big and warm… I didn’t think I’d like this, but… I do."

    # Image 60
    # Alina starts stroking Crystal’s cock more confidently, her hand moving up and down the shaft.
    scene d6toilet060 with dissolve
    w "It’s getting even harder in my hand…"

    cryst "Mmm… just like that, baby. Your hand feels so good. Keep stroking me."

    # Image 62
    scene d6toilet062 with dissolve
    w "[player_name]… can I… use her? I want to try more…"

    mc "You really want to?"

    w "Yes… I think I do."

    # Image 64
    scene d6toilet064 with dissolve
    cryst "Then take your clothes off for me, pretty girl. I want to see all of you too."

    w "Okay… I’ll do it."

    # Alina begins undressing, removing her top and then her skirt and underwear until she’s completely naked.

    # Image 66

    scene d6toilet066 with dissolve
    cryst "[player_name], please stay. I want you to watch this."

    w "yes… please stay. I’m… really nervous, but I want you here."

    mc "I’m not going anywhere."

    # Image 68
    scene d6toilet068 with dissolve
    cryst "Look at us, [player_name]. Two naked girls ready to give you a show you’ll never forget."

    w "We’re all yours to watch…"

    # Image 70
    # Alina drops to her knees in front of Crystal. Crystal gently holds the back of Alina’s head.
    scene d6toilet070 with dissolve
    cryst "Go on, baby. Take it in your mouth. I want to feel those pretty lips around me."

    w "It’s so big…"
    # Alina leans forward and starts sucking Crystal’s cock, slowly at first.

    w "mmm… slurp…"

    cryst "That’s it… good girl. Just like that."

    # Image 72
    # Alina bobs her head faster, taking more of Crystal’s length, clearly getting into it.
    scene d6toilet072 with dissolve
    cryst "Fuck… you’re sucking me so well, Alina. Your mouth feels incredible."

    w "Mmmph… gluck…"

    cryst "Yes… keep going. You’re making me so hard."

    # Image 74
    # Alina pulls back briefly, stroking Crystal with her hand, then slips two fingers between Crystal’s legs, teasing her pussy.
    scene d6toilet074 with dissolve
    w "Can I touch you here too?"

    cryst "Yes—finger me while you suck. I want to feel you everywhere."

    # Alina takes Crystal back into her mouth while sliding her fingers inside her.

    cryst "Oh fuck—yes, just like that… you’re such a quick learner."

    # Image 76
    # Alina pushes deeper, trying to take more of Crystal’s cock down her throat.
    scene d6toilet076 with dissolve
    cryst "Deeper, baby—take me deeper. You’re doing so fucking good…"

    w "gluck… gluck-gluck… mmmph!"

    cryst "That’s my good girl… choke on it if you have to. I love how eager you are."

    # Image 78
    scene d6toilet078 with dissolve
    cryst "You ready for me, baby? I’m going to fuck you… nice and deep."

    w "Yes… please… I want to feel you inside me."

    # Crystal slowly pushes forward, sliding her thick cock into Alina from behind.
    scene d6toilet080 with dissolve
    w "Oh my god… you’re so big… filling me up…"
    cryst "Fuck… you’re so tight and wet. Taking me so well."

    # Image 84
    # Both women turn their heads to look directly at MC, eyes full of lust.
    scene d6toilet084 with dissolve
    cryst "[player_name]… come here. Join us."

    scene d6toilet082 with dissolve
    w "Please… we want you too… come play with us…"

    menu mc_participate:
        "Join Alina and Crystal":
            mc "I’m in. I can’t resist you two any longer."

            cryst "Good boy. Come fuck us."

            scene d6toilet090 with dissolve
            # Image 90
            mc "Fuck it… I’m in. I can’t hold back anymore."

            cryst "Good boy. Get ready to feed Alina. She’s been such a good girl… she deserves a nice, thick load."

            # Image 100
            # Crystal is behind Alina, thrusting slowly into her from behind. Alina is on all fours, moaning.
            scene d6toilet100 with dissolve
            w "Crystal… you’re so deep… but I want [player_name] in my mouth too…"

            # Alina shifts, turning to sit on the floor between Crystal’s legs, still impaled on her cock.

            w "This way… I can suck you better while she fucks me."
            scene d6toilet110 with dissolve
            # Image 110
            # Crystal is now lying on her back on the bathroom floor. Alina is sitting on her cock, riding her slowly. MC stands in front of Alina.

            cryst "Ride me, baby… bounce on my cock while you suck him."

            w "Mmmph… so full… both of you inside me…"

            # She bobs her head on MC while grinding down on Crystal, taking both at the same time.

            # Image 115
            scene d6toilet115 with dissolve
            cryst "Fuck— I can’t hold it— I’m gonna come—!"

            # Crystal tenses, moaning loudly as she releases deep inside Alina, filling her with long, powerful pulses.


            scene d6toilet126_0 with dissolve
            w "Mmmph—!"

            scene d6toilet126 with dissolve
            cryst "YES!!! Take it all!"
            w "Fuck! You're coming so deep inside me!"

            scene d6toilet125_2 with dissolve
            # Image 125_2
            w "Mmm… now we both want to make you feel good…"

            cryst "That’s right… two mouths and four hands just for you. Look at us while we please you."

            # Image 130
            scene d6toilet130 with dissolve
            w "We’re ready… come for us. We want your load."

            cryst "Paint us, [player_name]. Cover our faces and tits. We want to wear you."

            # Image 132
            # MC groans and starts to climax. The first powerful ropes shoot across Crystal’s face and chest.
            scene d6toilet132 with dissolve
            cryst "Yes—give it to me—cover my face… fuck, there’s so much!"

            w "Look at you… covered in him. So pretty…"

            # Image 134
            scene d6toilet134 with dissolve
            w "My turn now… I want it too. Cover me while she’s still dripping with you."

            cryst "Go on, [player_name]. Give our pretty girl what she’s begging for."

            # Image 138
            # MC turns slightly and releases the rest on Alina’s face and breasts.
            scene d6toilet138 with dissolve
            w "Oh god—yes—give me all of it… I love feeling you explode on my face!"

            # Image 142
            # Both women turn to face each other, faces and chests covered in MC’s release, breathing heavily and smiling with satisfaction.
            scene d6toilet142 with dissolve
            w "We look so dirty… and so good together."

            cryst "Mmm… we do. Best team ever."

            # Image 144
            scene d6toilet144 with dissolve
            w "That was… amazing. Thank you, [player_name]."

            cryst "You really gave us everything… we’re both exhausted, but so happy."

            # Image 145
            # Alina and Crystal turn to each other and share a slow, deep, messy kiss.
            scene d6toilet145 with dissolve
            w "Mmm… we taste like him."

            cryst "I like it."

            # MC starts getting dressed.
            scene d6toilet147 with dissolve
            mc "I have to go now, but I’ll see you both tonight at the Show Bar. Don’t be late."

            # After MC leaves


            cryst "I’ll be there helping as a waitress. I’m good at keeping the energy high and the drinks coming."
            scene d6toilet148 with dissolve
            w "And I’ll go too. I may not be the best waitress, but I can at least help make the bar look full and fun."

            cryst "We’ll make sure it’s a night to remember."


        "Leave":
            mc "As much as I’d love to join you two right now… I really have to go. Rachel and Lucy are waiting for me back at the apartment."


            scene d6toilet094 with dissolve
            cryst "Aww, you’re really going to leave us like this? All hot and ready for you…"

            scene d6toilet095 with dissolve
            cryst "Fine, go be responsible. But next time you’re not getting away so easily, handsome. We’ll be waiting for you."
            w "[player_name]… you’re really leaving now? While she’s still… ahh… fucking me?"
            mc "I’ll message you both later with the details for the party at the bar tonight. Make sure you come."

    return



################### DAY 5 #################################
label morning5:
    play music musica5 loop
    scene d5apart020_2 with dissolve
    r "[player_name]… hey, sleepyhead. Time to wake up. I just wanted to let you know I’m heading out for a couple of hours."
    mc "Out? Where?"

    scene d5apart030_2 with dissolve
    r "I’m meeting an old friend for coffee. She lives nearby and texted last night. I thought it would be nice to catch up."
    mc "Sounds good. You deserve some friend time."

    scene d5apart032_2 with dissolve
    r "Thank you. Lucy’s already up and full of energy, so… you two have the morning to yourselves: go to the beach, explore the village, whatever you want. Just… behave. Both of you."
    mc "We’ll be angels."

    scene d5apart040_2 with dissolve
    r "I’ll be back by early afternoon. Maybe we can do something together later, like go to the cinema."
    mc "Sounds perfect. Have fun with your friend."

    scene d5apart060_1 with dissolve
    l "Mom’s gone! Morning just got way more fun."
    mc "Hey, trouble. You’re up early."

    scene d5apart070_1 with dissolve
    l "Duh! No mom means we’ve got the whole morning. Beach? Now? Come on!"
    mc "Already? You’re not even dressed yet."

    scene d5apart090_1 with dissolve
    l "This is dressed. Five minutes, trunks, let’s go. The beach's waiting."
    mc "Alright, you win. Give me three minutes to change."

    scene d5apart078_1 with dissolve
    l"Two! I’m timing you, handsome!"


    scene d5beach010 with dissolve
    mc "Hey… you’ve been quiet for a while. What’s up?"
    l "It’s… my adult account. It’s not doing great anymore."
    mc "What do you mean?"


    scene d5beach020_2 with dissolve
    l "Subscribers are dropping. Every week fewer people pay. And there are so many other girls doing the same thing now—better lighting, crazier outfits, collabs… I feel like I’m disappearing."
    mc "I’m sorry, Lucy. I know you put a lot into it."

    scene d5beach022_2 with dissolve
    l "No matter what I try, I can’t seem to prevent subscribers from dropping off."
    mc "That sucks. You must feel stuck."

    scene d5beach024 with dissolve
    l "Yeah. I don’t know what else to do. I can’t keep losing followers… it’s starting to feel pointless."
    mc "What if we tried someone else? Someone who’s already comfortable being bold in front of a camera."

    scene d5beach026 with dissolve
    l "Like who?"
    mc "Claudia. She’s got no problem showing off. Maybe she’d be up for a private shoot with you...something exclusive for your page."

    scene d5beach028 with dissolve
    l "Claudia…? You think she’d say yes?"
    mc "Only one way to find out. I can call her right now if you want. No pressure."

    scene d5beach029 with dissolve
    l "…Okay. Yeah. Call her. If she says yes… that could actually save everything."

    scene black5_01 with dissolve
    centered "A few minutes later..."

    scene d5beach025_2 with dissolve
    c "Well, hello, my favorite beach bunnies! I got your call, [player_name]. Couldn’t resist a morning dip with you two."
    scene d5beach031 with dissolve
    l "Hey, Claudia. Thanks for coming so fast."

    scene d5beach030 with dissolve
    c "Of course. You sounded desperate for help with your little… side project."

    scene d5beach035 with dissolve
    l "Yeah… my adult fanpage is losing subs fast. I need something big to bring people back."
    mc "We thought a shoot with you might work. I guess you’re comfortable in front of a camera, and… well, you’re stunning."

    scene d5beach040 with dissolve
    c "Flattery will get you everywhere, darling. But let’s be honest—this sounds deliciously naughty. I’m in."

    scene d5beach045 with dissolve
    c "There. No secrets between us. Now tell me—what kind of shots are we talking? Tasteful? Filthy? Somewhere deliciously in between?"

    scene d5beach050 with dissolve
    l "Oh my god… you’re perfect. Like… seriously perfect."


    scene d5beach065 with dissolve
    c "Then let’s not waste daylight. Where do you want me first, Lucy? And [player_name], you’re directing and shooting?"
    mc "Yeah. Phone’s ready. Let’s start with some natural poses...then we go bolder."

    scene d5beach055 with dissolve
    l "Okay… if we’re really doing this, fair is fair. No more hiding. Let’s do this."

    scene d5beach060 with dissolve
    c "That’s my girl. Confidence looks good on you, Lucy. Come here, let's pose together."

    scene d5beach105 with dissolve
    mc "Ready? Natural and cute first."
    mc "Got it. Smile, ladies—perfect!"

    scene d5beach106 with dissolve
    mc "Lucy… what if we make this even bigger for your fans?"
    l "Bigger how?"
    mc "Introduce Claudia to your followers properly. Not just random shots—make it a reveal. Start with her back—build the tease—then turn her around for the full front view."

    scene d5beach107 with dissolve
    l "Oh my god… yes. Like a slow reveal. Show her ass first, let them guess… then boom—those huge tits."
    c " I love the drama of it. Tease them with the back view… then give them everything."
    scene d5beach109 with dissolve
    mc "Okay—let’s do it right now. Claudia, turn around first, show that gorgeous ass."

    scene d5beach290 with dissolve
    c "Like this, darling?"
    l "Perfect… caption can be something like ‘Guess who joined me today? Hint: curves for days…’"


    scene d5beach292 with dissolve
    mc "Good, now a side angle, just enough to tease the profile of her breast but no full reveal yet."
    l "They’re gonna lose their minds wondering…"


    scene d5beach296 with dissolve
    c "Ready for the main event?"
    l "Yes—turn around. Give them the full Claudia."


    scene d5beach295_2 with dissolve
    c "Hello, Lucy’s fans… like what you see?"
    #l "Oh my god—yes! These are gold. Caption: ‘Meet my new collab queen. She’s BIG energy.’"
    mc "That’s going to bring subscribers back in droves."

    mc "{i}(I could tell Lucy to go bolder and see where this goes, or I could play it safe){/i}"
    menu:
        "Encourage Lucy to go bolder":
            jump go_bolder

        "Play it safe":
            jump play_safe

    return




label go_bolder:
    scene d5beach295_3 with dissolve
    mc "We’ve got some great shots… but I’m thinking we could push it further if you’re both up for it."

    scene d5beach365 with dissolve
    l "Bolder… yeah. I want that. I want them begging for more."
    c "You sure, baby? We can stay sweet… or we can give them something unforgettable."

    scene d5beach355 with dissolve
    l "Unforgettable. What do you think would look hottest?"
    c "Mmm… let’s show them every gorgeous angle of you. We start with you bending over for them…"

    scene d5beach350 with dissolve
    l "That sounds… so intense. But I want it. Show me off. Make them obsessed."
    c "That’s my brave girl. [player_name], get ready. We’re giving them a show."
    mc "Start whenever you’re ready. First pose—bending over. Claudia, guide her."

    scene d5beach425 with dissolve
    c "Arch that back, sweetie. Push it out for the lens. Show them how perfect this little ass is."
    l "Like this…?"
    mc "Perfect. Hold it… got it."

    scene d5beach415 with dissolve
    c "Open a little more… yes. Look at that pretty pussy glistening in the sun. So sweet, so inviting."
    l "Oh god… this feels so exposed…"
    mc "Beautiful. Stay there… snapping now."


    scene d5beach430 with dissolve
    c "Last one. Bend over again, but this time I’m right behind you, pulling you back against me."
    l "Claudia… I’m so wet right now…"
    mc "Hold that pose… incredible. Got it."


    scene d5beach470 with dissolve
    l "Claudia… that was insane. You made me feel so… wanted."
    c "You are really wanted, baby girl."

    scene d5beach477 with dissolve
    l "I want to feel how wet you are…"
    c "Mmmmm"


    scene d5beach480 with dissolve
    c "Fuck—yes… just like that, baby…"
    l "You’re so fucking wet… dripping down my hand…"

    scene d5beach479 with dissolve
    c "Faster… curl them… hit that spot—"
    l "Come for me… come all over my fingers…"

    scene d5beach481 with dissolve
    c "I’m...fuck! I’m close! don’t stop!"

    scene d5beach483 with dissolve
    c "{b}YES! FUCK!{/b}"

    # Her orgasm pulses through her, slick coating Lucy’s hand. Claudia shudders, thighs trembling, until she finally collapses back onto the sand, panting.
    scene d5beach485 with dissolve
    c "You’re a little devil… and I fucking love it."
    l "And you’re a fucking goddess… I’m already addicted to you."

    scene d5beach490 with dissolve
    c "So… [player_name], be honest. Did you enjoy the little show your girls just put on for you?"
    mc "Every fucking second. Couldn’t look away."
    l "It was… my first time touching another pussy. Claudia’s was so wet and hot… I didn’t expect it to feel that good."

    scene d5beach485_2 with dissolve
    c "First time, huh? You were a natural, baby. Made me come so hard I saw stars."
    l "I… I loved it. I want to do it again. Soon."

    scene d5beach490_2 with dissolve
    c "Hear that? Your little devil’s got a taste for pussy now. Better keep up."
    mc "Noted. I'm fucking thrilled you finally got to taste pussy… and starting with Claudia? Perfect choice."


    scene d5beachkiss010 with dissolve
    c "Come here, sweet girl."
    l "You’re… so beautiful."

    scene d5beachkiss015 with dissolve
    l "I could do this forever…"
    c "Then don’t stop. Kiss me again."
    play sound "kiss.mp3"

    jump sara_arrives

    return


label play_safe:

    scene d5beach270 with dissolve
    mc "Claudia, Lucy, stand back-to-back for me, shoulders touching, nice straight posture…"
    l "Mmm, Claudia… your skin feels so hot against mine. Ready to show [player_name] how perfectly our curves line up?"
    c "Oh, baby girl, I’m ready. Bend with me—let him see how juicy we look together."

    scene d5beach280 with dissolve
    c "I hope you enjoy watching us pose for you."
    mc "Trust me, I’m enjoying it way too much."
    #l "Thanks, this shoot turned out hotter than I ever dreamed, and I couldn’t have done it without you two"

    scene d5md010_2 with dissolve
    l "Claudia… thank you. Seriously. These shots are going to change everything for me."
    c "You’re very welcome, baby girl. You were incredible out there—brave, beautiful, natural."

    scene d5beach200 with dissolve
    l "You’re the gorgeous one. I mean… look at you. Your body is unreal. Especially… your tits. They’re so huge and perfect. I’ve never seen anything like them up close."
    c "You’re sweet. Go ahead. Touch. Feel how real they are."

    scene d5beach450 with dissolve
    l "Oh my god… they’re so soft… and heavy…I can’t believe I’m touching them."
    c "Mmm… that’s nice. Keep going if you want."

    scene d5beachkiss010 with dissolve
    c "You’re adorable."
    l "Mmm…"

    # The kiss lingers—warm, slow, exploratory. Breasts press together, skin on skin.
    scene d5beachkiss015 with dissolve
    play sound "kiss.mp3"
    c "Mmm… you kiss even better than you pose."
    l "That was… wow. I didn’t expect—"

    jump sara_arrives

    return


label sara_arrives:


    scene d5beach_sara_arrives with dissolve
    sar "Um… h-hi everyone… sorry if I’m interrupting…"
    l "Sara?! Oh my god—hi!"
    c "Hey, cutie. Perfect timing. Join the party?"

    scene d5beach_sara010 with dissolve
    sar "I-I was just… walking… and I heard voices… um… what’s… what’s going on here?"

    scene d5beach_trio020 with dissolve
    l "We’re shooting some fresh pics for my adult page again. Don’t worry, it’s all fun and super hot. Claudia was helping me with some… collab content."
    c "We were just getting to the good part. You’re welcome to watch… or join."


    scene d5beach_trio030 with dissolve
    mc "… these shots with Claudia are already incredible, but I can feel we’re just scratching the surface. What if we went full 'nasty' for the fans? You, Claudia, and Sara—all three of you together."

    scene d5beach_sara020 with dissolve
    sar "I… I don’t know if I can. You two are so… confident. My tits are tiny. I’d look like a kid next to Claudia. No one wants to see that."
    c "Bullshit. Sara—your shy, sweet tits and that innocent face? That’s pure fucking gold."
    mc "She’s right. Fans don’t want just huge tits—they want variety. Lucy’s filthy energy, Claudia’s curves, your sweet shyness... Together you’re a wet dream."

    scene d5beach_sara030 with dissolve
    sar "But… I’ll look stupid. Flat. Ugly next to..."

    #NOVA Cluadia holding tits
    #c "Feel these? Yeah, they’re big. But yours are perfect for pinching, sucking, making hard in seconds. Different weapons, same war. You in?"
    l "Come on, Sara. Get naked with us."

    scene d5beach_sara040 with dissolve
    sar "…Fuck it. Okay. I’ll do it."


    scene d5_beach_no with dissolve
    c "Strip, baby. Time to make some cocks explode."
    sar "I… okay… just the top first…"

    # Sara’s fingers fumble with the straps of her one-piece swimsuit. She slowly pulls the top down, letting it peel away from her small, perky breasts. Her nipples are already stiff from nerves and the sea breeze.

    scene d5beach_no4 with dissolve
    sar "They’re… too small. Nothing like yours or Claudia’s…"
    scene d5_beach_no2 with dissolve
    c "Stop that. Size doesn’t matter!. Now, everything else. Bottoms too. Like Lucy and me. Full nude. Show us that pretty pussy, baby girl."

    scene d5beach_no5 with dissolve
    sar "You really want to see… all of me?"
    c "Yes. Every inch. No hiding. Let us look at you the way you deserve to be looked at."

    # Sara stands up slowly. Her thumbs hook into the sides of her swimsuit bottom. She hesitates, then pushes it down her hips, letting it slide past her thighs and pool at her feet.
    scene d5beach_no6 with dissolve
    sar "Okay… it’s off. Everything. I’m… naked now. I can’t believe I’m doing this…"

    # She stands bare—small breasts, flat stomach, neatly trimmed patch above her pussy, legs pressed together nervously.

    scene d5beach_no7 with dissolve

    l "You look so pretty, Sara. Really. The fans are gonna love this. Thanks"

    scene d5_beach_no12 with dissolve
    c "You’re doing great already. Now let’s make it special for your page—just like we did with me."
    #mc "Same idea works perfectly here. We introduce Sara slowly. Start with the back—let them see that cute little ass first. Build the tease. Then turn her around for the full front reveal."
    l "Yes! Tease them with the back view. Make them guess what’s coming."
    sar "Just… the back first? Okay… I can do that."

    scene d5beach_no9_3 with dissolve
    l "Perfect! Caption can be ‘Guess who’s joining the fun today? Hint: sweet little surprise…’"
    mc "Sara… turn around slowly for me now. Let’s go from that sweet little ass to the full front view—show them everything, nice and easy."
    sar "They really want to see… more?"
    c "Let them see those pretty pink nipples and that sweet pussy."

    scene d5beach_no9_2 with dissolve
    sar "Okay… here goes."
    l "Fuck yes—look at you! So cute and innocent. Caption: ‘Meet my new shy collab queen. Tiny tits, big surprise…’"
    mc "Hold that pose… chin up, shoulders back. Beautiful. Got it."

    scene d5_beach_no10 with dissolve
    sar "They… they won’t think I’m too small?"
    c "Not a chance. They’ll be obsessed with how real and soft you are. You’re perfect like this."
    mc "You look amazing, Sara. All three of you do."

    scene d5_beach_no10_2 with dissolve #or 10_3
    l "You're posing so good with me, Sara… I'm super excited to have you right by my side like this."
    sar "T-thanks, Lucy… I’m really nervous, but… I’m glad I’m here with you too."

    #scene d5_beach_no12_2 with dissolve
    scene d5_beach13_1 with dissolve
    c "Hey [player_name]… we’ve got a situation over here. Sara’s been staring at your crotch the whole shoot like it’s the main attraction."
    scene d5_beach13_2 with dissolve
    sar "Claudia!! I-I wasn’t...! I mean...oh god..."
    l "Come on, admit it, Sara. You’re dying to see what’s under those trunks."

    scene d5_beach_no14 with dissolve
    sar "I… maybe… a little…"
    c "Then let’s give the girl what she wants. [player_name], lose the trunks. Get naked with us. Sara deserves a full view after being so brave today."
    l "Yeah… strip for us. Show Sara—and me—what you’ve been hiding all morning."


    menu:
        "Get naked too":
            jump get_naked_too

        "Nah, I’m good – let’s keep this shoot classy":
            jump shoot_classy

    return


label shoot_classy:


    mc "Appreciate the invite, but I’m staying Team Swimsuit today. Someone’s gotta hold the camera steady."

    scene d5triotalk040 with dissolve
    sar "Oh… okay, I guess I was hoping to see more…"

    scene d5triotalk050 with dissolve
    c "Aww, come on… we were all getting excited for the full view. Maybe next time you’ll let us unwrap the present."


    scene d5triotalk030 with dissolve
    l "Hey… I’ve got an idea.This is it—this is the content we’ve been missing! Claudia, Sara, you two together? Absolute goldmine for the fanpage!"

    scene d5triotalk060 with dissolve
    l "C’mon, camera king! You’ve gotta capture this. Claudia + Sara duo shots right now, pretty please?"
    c "She’s not wrong. Let’s give the fans what they’re begging for."
    sar "O-okay… if you both think it’ll be good… I’ll do it."

    scene d5triotalk070 with dissolve
    mc "Alright, you heard the boss. Face me, shoulders touching…"

    # Click! (First pic: Sara’s biting her lip a little, eyes glancing down shyly, Claudia looking confident and sultry right beside her)


    scene d5triotalk090 with dissolve
    mc "Sara, hit me with the full happy-sunshine smile. Claudia, keep owning it."


    scene d5triotalk099 with dissolve
    mc "Wait...Lucy? Are you… taking pictures of me now?"

    scene d5triotalk097 with dissolve
    l "Yup! Gotta have memories of today too, y’know?"
    mc "You’re sneaky. I didn’t notice you."


    scene d5triotalk095 with dissolve
    c "Awww, Lucy’s making a whole ‘behind the scenes’ collection."
    sar "Or just… y’know… to remember how hot our photographer was that day."
    l "Exactly. Memories. That’s all..."

    jump d5_beach_end2
    return



label get_naked_too:
    scene d5_inici_trio with dissolve
    mc "Alright… you asked for it."
    l "Holy shit… look at that thing. Thick as my wrist."
    c "Look how hard he is already—poor boy’s been suffering watching us all morning."
    sar "It’s… really big… and it’s twitching…"
    scene d5_inici_trio03 with dissolve
    l "Who’s gonna take care of that for him? He’s practically leaking already."
    c "I say we let the shy one do the honors. Sara’s been staring at it like she wants to worship it."
    sar "M-me?! I… I don’t have much experience with men… or cocks… this is only the second one I’ve ever seen up close."

    scene d5_inici_trio02 with dissolve
    l "Come on, Sara. You want it. We can all see it in your eyes."
    c "I’ll help you. Guide your. Show you exactly how he likes it. We’ll make him come so hard he forgets his own name."
    sar "I… okay. I want to. But… you’ll really help me?"

    scene d5inici_trio04 with dissolve
    c "Spread your legs a little, sweetie. Let him look. Let him want you."
    sar "I… okay…Like this...?"
    l "Damn right. Sara, you’re making him throb..."

    scene d5_inici_trio05 with dissolve
    c "Perfect. [player_name]—take a good look. See how pretty she is? Those sweet little tits, that pink pussy already glistening…"
    sar "I… I like that he’s looking."

    scene d5_inici_trio06 with dissolve
    c "Come on, sweetie… right here. Face him. Let him see how brave you are."
    l "O-okay…"

    scene d5_inici_trio07 with dissolve
    c "Good girl. Now look at that big, hard cock. Isn’t it impressive?"
    sar "It’s… really big… and it’s moving…"

    scene d5_inici_trio08 with dissolve
    c "See? Nice and warm. Don’t be shy—lean in a little. Just close enough to feel the heat."
    sar "Claudia… it’s right there…"

    scene d5beach_new010 with dissolve
    c "Mhm. Smell it? All that man right in front of your pretty face."
    sar "It’s… kinda salty… and warm…"

    scene d5beach_new020 with dissolve
    c "Together now… slow licks, bottom to top. Just teasing him."
    sar "That… is fun. He’s twitching so much…"

    scene d5beach_new030 with dissolve
    c "Told you. Nothing more fun than teasing a hard cock together."
    mc "You two are gonna kill me…"

    scene d5beach_new040 with dissolve
    c "Okay, Sara… you’re on your own now. Take him nice and slow. You’ve got this."
    sar "slurp...slurp"



    scene d5beach_new055 with dissolve
    c "That’s it, sweetie… don’t rush him. Make him ache for your mouth. He loves it when you play shy but naughty."
    sar "Mmm… you taste salty… and hot…"


    scene d5beach_new060 with dissolve
    c "Good girl… take a little more. Feel how he throbs when you suck harder."
    sar "mmmph… slurp… gluck…"


    scene d5beach_new070 with dissolve
    c "Oh my god, Sara—look at you taking him so deep! I didn’t think you had it in you, baby girl… I’m honestly shocked and so fucking proud!"
    l "Fuck… Sara… that’s incredible…I need to capture it!"
    sar "gluck-gluck… mmmph…"



    scene d5beach_new097_3 with dissolve
    c "You are a natural. Faster now, Sara… make him lose control."
    sar "slurp, slurp, gluck… mmm…"
    mc "Fuck… Sara—I’m close…"

    scene d5beach_new100 with dissolve
    l "Yes… give the camera that moment…"
    sar "YES! Oh… so much… it’s everywhere…"

    scene d5beach_new105 with dissolve
    c "You did amazing, sweetie. Look at him—he’s still shaking."
    l "You’re a star, Sara."
    sar "I… I liked it. A lot."

    scene d5beach_new120 with dissolve  #115 tambe
    mc "Hey, Lucy… those last pics and videos? Please don’t post them anywhere. Keep them just between us, okay?"
    l "Don’t worry, [player_name]. They’re only for me, my personal little collection. No one else will ever see them. Promise."

    jump d5_beach_end
    return


label d5_beach_end:

    scene d5_fb020 with dissolve
    c "You were so brave today, sweetie… look at you standing here naked with me. No hiding."
    sar "I… I still feel tiny next to you, but… thank you for making me feel like I belong."

    scene d5_fb010 with dissolve
    c "See her, [player_name]? She’s perfect just like this—small tits, sweet curves, all real. She’s a treasure."
    sar "Do… do you really think so too, [player_name]?"
    mc "Absolutely. You’re beautiful, Sara. Every part of you. Don’t ever doubt it."


    scene d5_fb030 with dissolve
    l "Oh! Mom just texted—she’s already at the cinema waiting for us. Says she got the tickets for that rom-com she wanted to see."
    mc "Nice. We should probably head straight there then."


    scene d5_fb040 with dissolve
    l "Yeah… but first, I was just looking at those last pics we took. Some of them have {b}you{/b} in the background, y’know."
    mc "Lucy… those ones with me in them? They can’t go on your fanpage. I’m okay with you keeping them, but they stay private. Just for you."


    scene d5_fb055 with dissolve
    l "Don’t worry, handsome. They’re only for me. My little secret collection… no one else gets to see you like that but me."
    mc "Good. That’s all I ask."

    return



label d5_beach_end2:

    scene d5_fb030 with dissolve
    l "Oh! Mom just texted—she’s already at the cinema waiting for us. Says she got the tickets for that rom-com she wanted to see."
    mc "Nice. We should probably head straight there then."


    scene d5_fb040 with dissolve
    l "Those last pics are my favorite—Claudia and Sara together while you were snapping away? So hot and powerful. I’m already replaying them in my head!"
    mc "Lucy, those shots with me in them can’t go on your fanpage. You need to delete them—keep it private, okay?"


    scene d5_fb055 with dissolve
    l "Relax, handsome. They’re staying in my private collection forever—just for me."
    mc "Good. That’s all I ask."

    return



label cinema5:

    scene blackd507 with dissolve
    centered "You, Lucy, and Rachel pull up to the cinema."

    scene d5cinema005 with dissolve
    mc "Wow… this place is almost empty. Feels like we’ve got the whole cinema to ourselves tonight."

    scene d5cinema010 with dissolve
    l "Yes, this place is basically ours! Only like five other people here."
    r "Perfect. No one to shush us if we whisper too much."

    scene d5cinema060 with dissolve
    r "Middle row is perfect!"
    l "Good choice mom."

    scene d5cinema065 with dissolve
    mc "{i}(Damn… those tits are unreal.){/i}"
    # One wears a tight, low-cut red dress that barely contains her massive cleavage; the other has a sparkling black halter top with a deep plunge, breasts spilling over.

    menu cinema_peek:
        "Sneak a quick peek at the two busty women in front":
            # MC’s eyes drift downward for a moment, lingering on the deep cleavage and the way their breasts rise and fall with each breath.
            scene d5cinema070 with dissolve
            mc "{i}(The pink dress is fighting for its life—look at how they’re spilling out, jiggling with every little move.){/i}"

            scene d5cinema075 with dissolve
            mc "{i}(Fuck, those deep cleavage is practically begging to be stared at. Hard not to get distracted.){/i}"

            scene d5cinema077 with dissolve
            l "Caught you! Staring at the big-titty front-row show, huh? Can’t blame you… those dresses are barely holding on."
            mc "Busted."


        "Keep your eyes on Rachel and Lucy, ignore the front row":
            # MC keeps his gaze on Rachel and Lucy, smiling at them instead.

            scene d5cinema077 with dissolve
            l "Those two in front are basically spilling out of their tops—thought you’d at least sneak one look, Mr. Polite."
            mc "Nah, I’m good right here. Got the best view in the theater sitting next to you."

    scene d5cinema078 with dissolve
    l "Hey, check out the girl behind you. She hasn’t taken her eyes off you. Seriously, do you have some secret magnet for women or what?"

    scene d3cinema050 with dissolve
    mc "{i}(Wait… that’s Alina? Shit, I didn’t even clock her at first){/i}"

    scene d5cinema081 with dissolve
    l "Don’t worry, I won’t tell Mom… but you owe me later for keeping your little secret."

    scene d5cinema079 with dissolve
    r "Shh, previews are starting."

    scene d5cinema082_2 with dissolve
    pause 2.0

    scene blackd505 with dissolve
    centered "The movie played out quietly."


    scene d5cinema085 with dissolve
    r "That was nice. Quiet, no interruptions… perfect night out."
    l "Yeah, but now I’m starving. Can we grab something on the way home?"


    menu cinema_end_choice:
        "Leave with Rachel and Lucy":

            scene d5cinema087 with dissolve
            mc "Girls… I’m feeling like one last beer before we head back. There’s that little bar nearby—thought I’d stop in for a quick one."

            scene d5cinema089 with dissolve
            r "One last beer, huh? You sure you’re not just trying to avoid the walk home?"
            mc "Maybe a little. But seriously, I could use a nightcap. You two go ahead—I’ll catch up in a bit."

            #scene d5cinema091 with dissolve
            #l "Fine by me. More food for us!"

            scene d5cinema092 with dissolve
            l "Yes! See you later, [player_name]! Don’t do anything I wouldn’t do..."
            r "Don’t be long, okay? We’ll save you some food… maybe."
            mc "Promise. I’ll be home soon."

            return

        "Stay longer with an excuse":

            scene d5cinema087 with dissolve
            mc "Actually… I think there might be post-credits scenes. You two go ahead—I’ll catch up in a minute."

            scene d5cinema089 with dissolve
            r "Really? The credits looked finished…"


            scene d5cinema092 with dissolve
            l "Suuure, [player_name]. Take your time. Don’t do anything I wouldn’t do..."


            scene d5cinema094 with dissolve
            menu cinema_after_choice:
                "Go with the two busty girls":
                    scene d5cinemadana01 with dissolve
                    da "Name's Dana... y'know, if you're more interested in that than my rack."
                    scene d5cinemanoemi01 with dissolve
                    na "I'm Naomi… in case you're actually curious about my name and not just wondering how these girls stay so perky without any help."
                    scene d5cinema096 with dissolve
                    da "We promise you’ll have a good time. Very good."
                    mc "Yeah… I’m in."

                    # Alina watches from across the aisle. Her smile fades. She looks down, shoulders slumping.

                    scene d5cinema098 with dissolve
                    w "I guess I get it… why would you pick me when they have so much more to offer? My body’s just… nothing next to theirs."

                    scene d5cinema099 with dissolve
                    w "Have fun with them. I’ll go home and try to forget how ugly I feel standing next to girls like that. Goodbye, [player_name]."

                    # She turns and leaves quickly, head down, clearly unhappy.

                    # The two busty women link arms with MC, leading him toward the exit, laughing softly.
                    scene d5cinema097 with dissolve

                    jump dana_cinema

                "Go with Alina":
                    scene d5cinemaalina01 with dissolve
                    w "I did. I just… didn’t think you’d pick me over… them. The way they were dressed, those curves… I thought…"
                    mc "I wanted you. Not them. You."
                    scene d5alina010 with dissolve
                    w "That makes me… really happy. And… really turned on. I like doing it in public places. The risk… the thrill of almost getting caught. Right here. Right now. With you."
                    w "Come with me. Let me make you feel good."

                    scene d5cinema_leave02 with dissolve
                    da "Guess he’s got other plans tonight."
                    u "No biggie. More fun for us somewhere else."
                    jump alina_cinema

    return

label alina_cinema:
    w "Wait here… I want to do this right."


    w "No one’s here… but the thought that someone *could* walk in… it makes me so wet."

    # She reaches for the hem of her top and slowly pulls it over her head, revealing her medium breasts—nipples already hard from excitement and the cool air.
    scene d5alina015 with dissolve
    w "Look at me… really look."

    # Next she unbuttons her jeans, shimmying them down her hips along with her panties in one smooth motion. She steps out of them, now completely naked.
    scene d5alina020 with dissolve
    w "I want you to see everything…"

    # She bends forward slowly, hands resting on her knees, ass presented toward him. Her legs part slightly, pussy glistening in the faint screen glow, back arched to show off her curves.
    scene d5alina030 with dissolve
    w "Like this? Can you see how ready I am for you?"

    # She reaches back with one hand, spreading herself gently—lips parting, pink and slick.
    scene d5alina040 with dissolve
    w "Come closer… touch me… fuck me right here in front of the screen. The risk… it’s driving me crazy."

    # MC stands, moving down the aisle toward her, heart pounding as Alina stays bent over, fully exposed and waiting.
    scene d5alina045 with dissolve
    w "Please… take me. Right now. While the theater’s still ours."

    scene d5alina050 with dissolve
    mc "You sure about this? Right here… anyone could walk in."
    w "That’s what makes it so hot. Please… fuck me. Now."

    # MC moves behind her. He grips her hips, cock brushing against her wet entrance.
    scene d5alina060 with dissolve
    mc "Fuck… you’re soaked."
    w "Yes! Deeper… fill me up…"

    # He thrusts forward in one smooth stroke, burying himself to the hilt. Alina moans softly, hands gripping her knees for balance.
    scene d5alina075 with dissolve
    w "Like this… harder…"

    # MC starts moving—slow at first, then faster. Wet slapping sounds echo faintly in the empty theater as he pounds her from behind.
    scene d5alina070 with dissolve
    w "Oh god! yes! Just like that… fuck me like you mean it…"
    mc "You feel so fucking good… tight and wet…"

    scene d5alina082 with dissolve
    w "I’m close already… don’t stop—!"
    mc "Turn around. I want to see your face when you come."

    scene d5alina085 with dissolve
    w "Like this…?"
    mc "Yes..."
    # She spreads her legs wide. MC kneels between them, sliding back in easily. Alina wraps her legs around his waist, pulling him deeper.

    w "Yes! Look at me while you fuck me…"

    # MC thrusts hard and steady, hands braced on either side of her head. Alina’s breasts bounce with each movement, nipples hard.
    scene d5alina090 with dissolve
    w "I’m gonna come… keep going...harder!"

    # Her pussy clenches around him as her orgasm hits—back arching off the floor, a soft cry escaping her lips.
    scene d5alina092 with dissolve
    w "*Fuck! [player_name], yes!"

    # MC groans, thrusts growing erratic. He buries himself deep one last time, coming inside her with a low growl.
    scene d5alina094 with dissolve
    w "Wait… pull out for a second… I want to finish you with my mouth."
    mc "You sure? I’m close…"

    scene d5alina096 with dissolve
    w "Yes. I want to taste you when you come. I want it on my tongue… in my mouth."

    scene d5alina095 with dissolve
    w "Mmm… you taste like us…"

    # She starts bobbing—slow, deep strokes, tongue swirling along the underside. Wet sucking sounds fill the quiet theater.
    scene d5alina097 with dissolve
    w "mmmph… slurp… gluck…"


    scene d5alina100 with dissolve
    w "gluck-gluck… mmmph…"
    scene d5alina100 at Shake((2.5, 3.0, 2.5, 3.0), 3.0, dist=6)
    mc "Fuck! Alina...NOW!"

    scene d5alina105 with dissolve
    w "Mmm… so much… you taste so good…"
    mc "You’re unbelievable. That was… perfect."
    # She licks him clean—long, slow drags of her tongue from base to tip—then looks up at him with a satisfied, almost proud smile.
    scene d5alina115 with dissolve
    w "I love making you come like that…"
    mc "That was… incredible, Alina. But I really have to go. Rachel and Lucy are waiting for me back at the apartment."
    scene d5alina225 with dissolve
    w "I know… you told me. Go to them. They’re lucky to have you."
    mc "Hey… how about one last beer? There’s a quiet bar nearby. Just us, one drink before I head home?"

    scene d5alina220 with dissolve
    w "Tempting… really tempting. But no. I think I’d rather end the night like this: hot, breathless, and perfect."
    mc "Tonight was unforgettable, Alina… I’ll be thinking about you the whole way home."

    scene d5alina230 with dissolve #o 35 o 37
    w " …Best movie night ever."

    scene d5cinemaout with dissolve
    mc "{i}(One last beer before home… I think I earned it){/i}"

    return

label dana_cinema:
    da "You stayed with us… good choice."
    na "We were hoping you would. The movie was boring… but the after-party? That’s gonna be fun."

    scene d5cinema100 with dissolve
    da "You know what makes it better? The risk. Anyone could walk back in… and catch us."
    na "Exactly. That little thrill… it makes everything hotter."

    # Dana stands up slowly in the aisle, facing MC. She reaches behind her back and unzips her red dress.
    scene d5cinema105 with dissolve
    da "Watch me… I’m getting naked right here. The chance of someone seeing? Fuck, it turns me on."
    na "My turn…"

    # Naomi unties her halter top. It falls away, revealing massive, heavy breasts—dark nipples stiff. She shimmies out of her skirt and panties, thick ass and full pussy now bare.
    scene d5cinema120 with dissolve
    na "Look at all this… you like big girls, don’t you? We’re gonna make you feel so good."
    da "You’re staring so hard… like you’ve never seen tits this perfect before—don’t worry, they’re all yours to watch tonight."

    scene d5cinema125 with dissolve
    da "Your turn, handsome. Get naked. We want to see that cock."
    na "Yeah… strip for us. Let us taste you while the theater’s still quiet… for now."


    scene d5cinema130 with dissolve
    da "Fuck… look at that. Thick and ready."
    na "Mmm… I want the first lick."

    # Both women lean forward on their knees. They start at the base—tongues flat and slow, dragging up together from balls to tip.

    scene d5cinema132 with dissolve
    na "So good… taste him with me, Dana."
    da "Mmm… salty… hard… fuck, I love this cock."

    # Their tongues meet at the tip, sliding over each other as they lick him in unison—long, wet strokes, lips occasionally brushing, moans vibrating against him.

    scene d5cinema135 with dissolve
    da "You like watching us lick you together? Two hungry mouths on your dick?"

    scene d5cinema137 with dissolve
    na "We’re gonna make you come so hard…"


    scene d5cinema140 with dissolve
    na "Enough playing. Open that mouth, Dana. Suck his cock like the good little slut you are."
    da "Yes… Naomi…mmmph"

    scene d5cinema150 with dissolve
    na "Eyes on me, [player_name]—watch how eagerly my little slut opens wide for your cock… she’s gonna choke on it just the way I like."
    da "gluck… gluck-gluck… mmmph!"

    scene d5cinema145 with dissolve
    na "My turn to help."
    da "I… I love it… I love being used… *gluck*… I’m your good little sucker…"

    scene d5cinema142 with dissolve
    na "That’s it… take it all. You love this, don’t you? Being used like a dirty little toy."
    da "gluck-gluck-gluck… mmmph…"
    # Naomi kneels behind Dana, one hand still on the back of Dana’s head, the other sliding down to grab Dana’s hip for leverage.

    scene d5cinema147 with dissolve
    na "Mmm, look at her go… my good little cocksucker taking you so deep. Keep watching, baby—Dana loves being used just like this, and I love making her do it for you."

    #scene d5cinema180 with dissolve
    #na "Mmm… look at her. My girl knows exactly how to please a man when I tell her to."


    scene d5cinema151 with dissolve
    na "Just so you know… I prefer women. Always have. Men are fun, but pussy’s what really gets me wet."

    # She strokes Dana’s cheek affectionately while Dana continues.

    scene d5cinema152 with dissolve
    na "But I’ll let you have your fun with my girlfriend tonight. Fuck her… as long as she keeps pleasing me."

    # Naomi shifts forward, straddling Dana’s back facing MC. She spreads her thick thighs wide, pussy glistening, hovering just above Dana’s face.
    scene d5cinema154 with dissolve
    na "Tongue out, Dana. Lick me. Make me come on your pretty face."
    da "slurp, slurp"
    # Dana moans louder around MC’s cock—*gluck… mmmph…*—and tilts her head back slightly. Her tongue extends, flicking against Naomi’s swollen clit.
    scene d5cinema180 with dissolve
    na "Fuck… yes, just like that. Good girl… keep that mouth busy on me."

    # Dana alternates—sucking MC deep, then licking up Naomi’s slit, moaning the whole time.
    scene d5cinema160 with dissolve
    na "See how she trembles when she tastes me? She loves being used by both of us… don’t you, baby?"
    da "mmmph… yes…"

    scene d5cinema170 with dissolve
    na "Keep going… make him come while you eat my pussy. I want to feel you moan into me when he fills your pussy."
    mc "Shit… your pussy is so tight, Dana. And watching you eat her at the same time…"
    da "mmmph… slurp…"

    scene d5cinema171 with dissolve
    na "Fuck… yes, right there. Lap at it, baby… taste how wet you make me."

    # Dana’s tongue works faster—long, wet strokes up Naomi’s slit, circling the clit, dipping inside. Sloppy, hungry sounds fill the air.


    scene d5cinema172 with dissolve
    na "She loves it. My girl gets so fucking wet when she’s used like this."

    # Dana’s tongue plunges deeper, lips sucking at Naomi’s folds while her head still bobs on MC’s cock—alternating between the two.
    scene d5cinema173 with dissolve
    na "Don’t stop… fuck her harder while she fucks me with her tongue!"

    # MC thrusts gently into Dana’s throat. Dana gags softly—*gluck-gluck*—but keeps licking Naomi eagerly.

    scene d5cinema156 with dissolve
    na "I’m close… keep going Dana, eat my pussy."
    da "gluck… mmmph… slurp!"

    # Naomi’s thighs tremble. She grinds down one last time, crying out as her orgasm hits—pussy pulsing against Dana’s tongue.
    scene d5cinema155 with dissolve
    na "Fuck! Yes, right there! Ahhhhhhhh!"


    scene d5cinema185_1 with dissolve
    na "Good girl… now make him cum too…"

    scene d5cinema185 with dissolve
    na "Finish on her, [player_name]. Pull out and paint her pretty face and those fake tits. Cover my girl in your load."

    scene d5cinema195 with dissolve
    mc "Fuck...now..."
    da "Yes...yes...cum on me!"

    # MC pulls out of Dana’s mouth with a wet pop. He strokes himself fast. Dana tilts her face up, mouth open, eyes wide.
    scene d5cinema200 with dissolve
    mc "Here it comes!"
    da "Oh!"
    # Thick, heavy ropes erupt—first hitting her lips and cheek, then splashing across her face in hot streaks. More lands on her big fake tits, dripping down the curves and between her cleavage.
    scene d5cinema205 with dissolve
    da "Oh my god… there’s so much… it’s everywhere…"

    # Come drips from her chin onto her breasts; she blinks, shocked at the volume, some clinging to her eyelashes.
    scene d5cinema215 with dissolve
    da "I… I didn’t expect this much… "

    scene d5cinema225 with dissolve
    na "Thank you, [player_name]. You gave my girl a night she won’t forget."
    da "Thank you… that was… intense. And hot."
    mc "You two were… unbelievable. I should head out before someone walks in."


    scene d5cinema230 with dissolve
    na "Go on, handsome. We’ll clean up here. Come back anytime you want more."
    da "Night, [player_name]."

    scene d5cinemaout with dissolve
    mc "{i}(One last beer before home… I think I earned it){/i}"


    return




label evening5:
    scene bar_door with dissolve
    mc "{i}(Alright, let's see what kind of chaos this place is serving up tonight…){/i}"
    scene d5_night005 with dissolve
    mc "{i}(Wow… place is dead tonight.){/i}"

    scene d5_night010 with dissolve
    pause 2.0
    scene d5_night015 with dissolve
    mab "Come on in, [player_name]. First drink’s on the house."

    scene d5_night020 with dissolve
    mc "Thanks. Where is everyone? Thought this place usually had at least some regulars."

    scene d5_night025 with dissolve
    mab "Regulars only show up when Claudia’s dancing. Tonight she’s off. So… empty bar, empty pockets."

    scene d5_night030 with dissolve
    mab "Grab a stool. Actually… screw the stools. It’s totally empty. We can sit wherever we want."

    scene d5_night040 with dissolve
    mab "I keep thinking maybe I’m doing something wrong. The lights, the music, the drinks… but it’s always the same. Claudia performs—people come. Claudia rests—people stay home."
    mc "It’s not your fault. She’s got… star power."

    scene d5_night050 with dissolve
    mab " Star power. Yeah. And I’m just the one presenting and paying the rent. I love her, but sometimes I wish I had even half her pull."

    scene d5_night070 with dissolve
    mab "Sorry. I’m not usually like this. Just… tired. And the vodka helps. For a while."
    mc "You don’t have to apologize. Want to talk about it, or should I just sit here and keep you company?"

    scene d5_night065 with dissolve
    #mab "Sometimes I wonder if the bar’s even worth it anymore. If Claudia ever leaves… I don’t know what I’d do."
    mab "Two days. That’s all I’ve got. The rent, the liquor license renewal, the electric bill… it’s all due. If I can’t pay, the landlord takes the keys. Bar’s gone."
    mc "That’s rough, Mabel. How much are we talking?"

    scene d5_night075 with dissolve
    mab "Enough that I don’t have it. Not even close. I’ve been scraping by on Claudia’s nights… but it’s not enough anymore. I thought I could keep this place alive. Thought it was my dream. Now it feels like a trap."
    mc "You’re not losing it. Not if I can help it."

    scene d5_night060 with dissolve
    mab "What do you mean? You can’t just..."
    mc "I'll take care of it. We'll boost the revenue for tomorrow night's show. I'll make sure the cash flows in. You don't have to worry"


    scene d5_night078 with dissolve
    mab "[player_name]… that’s… thousands. You don’t even know how much—"
    mc "I don’t need to know the exact number yet. I have a plan. Trust me. I’ll handle everything."

    scene d5_night065_2 with dissolve
    mab "Why would you do that? You barely know me…"
    mc "I know you love this place. I know you’re fighting to keep it. That’s enough for me. Let me help."


    scene d5_night082 with dissolve
    mab "I don’t know what to say… thank you doesn’t even begin to cover it."
    mc "You don’t have to say anything right now. Just… keep the bar open. I’ll sort the rest."

    scene d5_night080 with dissolve
    mab "I will. I promise. And… when you’re ready to tell me the plan… I’ll be here."

    menu bar_choice:
        "Go home":
            mc "It’s getting late. I should probably head back to the apartment. Rachel and Lucy are waiting."

            scene d5_night085 with dissolve
            mab "Yeah… you’re right. Thanks for sitting with me tonight. It meant more than you know."
            mc "Anytime. I’ll take care of that bill. Don’t worry about it anymore."
            mab "I won’t. Goodnight, [player_name]."
            return

        "Tell Mabel she has nothing to envy from Claudia":
            mc "Mabel… listen. You’ve got nothing to envy from Claudia. She’s great on stage, sure, but you? You could be just as big. Maybe bigger."

            scene d5_night090 with dissolve
            mab "Me? Dancing? I’m not… I don’t have her confidence…"
            mc "You could light up that stage. I’ve seen how you move when you’re behind the bar or presenting. You’ve got rhythm. You’ve got fire. You just haven’t let it out yet."

            scene d5_night095 with dissolve
            mab "You’re crazy. But… maybe. Just maybe."
            mc "Think about it. The bar needs a new star. Why not you?"


            scene d5_night097 with dissolve
            mab "I’ll… think about it. Really think about it."
            mc "Good. And if you ever want to practice… I’ll be your first audience."

            play music musica_strip loop

            scene d5_night100 with dissolve
            mab "…You know what? Fuck it. If I’m going to lose this place in two days… I’m going to give you a show first. Just for you. Right now."
            mc "Mabel..."

            scene d5_night110 with dissolve
            mab "No. Don’t say anything. Just sit. And watch. I want you to look at me. Really look."

            scene d5_night115 with dissolve
            mab "This is my bar. My rules. Tonight… I dance for one person. You. Look at me… watch how I move. I’ve still got it, don’t I?"

            # She turns slowly, hands sliding up her sides, fingers catching the hem of her top.
            scene d5_night120 with dissolve
            mab "You said I have nothing to envy from Claudia… let’s see if you still think that when I’m bare."

            # The top comes off—her full, heavy breasts spill free, nipples already stiff from the cool air and adrenaline.
            scene d5_night125 with dissolve
            mab "Look at these tits. They’re real. They’re mine. And they’re dancing for you tonight."

            # She turns again, back to him, hands sliding down to the waistband of her skirt.
            scene d5_night135 with dissolve
            mab "And this ass… Watch it burn for you."

            # The skirt drops to the floor. She steps out of it, now only in panties—black lace that clings to her curves.
            scene d5_night140 with dissolve
            mab "See? Nothing to envy. Just a woman who still knows how to move."

            # She straightens, turning to face him fully. Fingers hook into the sides of her panties.
            scene d5_night140 with dissolve
            mab "Last piece. You ready to see all of me?"

            # She slides them down slowly, letting them fall. Now completely naked—curves, soft belly, trimmed patch above her pussy—all on display.
            scene d5_night145 with dissolve
            mab "There. All of me. No hiding. Just look, [player_name]. Look at the woman who’s still fighting for this place… and who is dancing naked for you."

            # She sways gently to the music, arms lifting, body rolling in slow, sensual circles—full breasts swaying, hips undulating, every movement deliberate and intimate.
            scene d5_night150 with dissolve
            mab "Do I still have it? Do I still make you want to watch?"
            mc "You’re fucking mesmerizing."

            scene d5_night155 with dissolve
            mab "Good. Then enjoy my body..."

            # Mabel finishes her final spin, arms raised, breasts swaying, hips still rolling gently to the fading beat.
            scene d5_night160 with dissolve
            mab "God… I haven’t danced like that in years. Felt your eyes burning into me."

            # She steps closer, completely bare, nipples hard, a sheen of sweat on her skin.
            scene d5_night162 with dissolve
            mab "I’m so fucking hot right now, [player_name]. My body’s on fire. I don’t want it to stop. I want more… I want you right here, right now."

            # She stands inches from him, thighs pressed together, breathing heavy.

            stop music fadeout 2.0
            play music musica5 loop

            menu mabel_choice:
                "Go further with Mabel":
                    mc "I also want more. A lot more. Right now."
                    jump mabel_further

                "Go home":
                    mc "You were incredible, Mabel. But I should head home. Rachel and Lucy are waiting."

                    scene d5_night164 with dissolve
                    mab "Fair enough. Thank you… for watching. For seeing me."
                    mc "Goodnight, Mabel. Keep fighting for this place."

                    scene d5_night166 with dissolve
                    mab "Goodnight, [player_name]. And...if you ever change your mind… the stage will always be open for you."

    return


label mabel_further:
    $mabel += 10
    $lust += 10
    #show screen lust10

    scene d5_night200 with dissolve
    mab "Good boy… come here and take what you want."

    # Mabel turns slowly, then bends forward over the table—hands flat on the surface, back arched, ass presented high.
    scene d5_night205 with dissolve
    mab "Come here, [player_name]… look at me like this."

    # She spreads her legs slightly wider, ass cheeks parting just enough to show her glistening pussy and tight rear entrance.
    scene d5_night207 with dissolve
    mab "See how wet I am? All from dancing for you… from feeling your eyes on every inch."

    # Her heavy breasts hang and sway beneath her, nipples brushing the cool tabletop.
    scene d5_night209 with dissolve
    mab "I want you inside me. Right here. Bend me over this table and fuck me like you own this bar… like you own me tonight."

    # She reaches back with one hand, spreading herself open—pussy lips swollen and slick, ready.

    scene d5_night212 with dissolve
    mab "Please… take me. Hard. Deep. Make me scream your name in my own damn bar."
    mc "You sure you can handle it, Mabel?"

    scene d5_night211 with dissolve
    mab "Try me. I need it. I need you."

    # MC grips her hips. The head of his cock presses against her entrance, teasing.
    scene d5_night214 with dissolve
    mab "Yes—push in… fill me up…"

    # He thrusts forward slowly at first—then harder, burying himself to the hilt in one smooth stroke.
    scene d5_night213 with dissolve
    mab "Fuck—yes! So deep… don’t stop!"

    # The table creaks under their rhythm. Mabel’s breasts slap against the wood with each powerful thrust.

    scene d5night220 with dissolve
    mab "Harder—pound me! Make my ass bounce for you!"

    # MC grips her hips tighter, slamming into her—wet slapping sounds echoing in the empty bar.
    scene d5night230 with dissolve
    mab "I’m—oh god—I’m gonna come!"

    # Her pussy clamps down hard around him as she orgasms—back arching violently, a raw scream tearing from her throat.

    scene d5night232 with dissolve
    mab "YES! FUCK!"

    scene d5night240 with dissolve
    mab "Don’t stop… "

    scene d5night245 with dissolve
    mc "I’m close… fuck—"

    # He pulls out suddenly with a wet sound, hand stroking fast. Mabel stays bent over, looking back over her shoulder with wide, hungry eyes.
    scene d5night246 with dissolve
    mab "Yes—on me… cover me…"

    # MC groans low. Thick, heavy ropes shoot out—first splashing across her lower back, then more landing on her round ass cheeks, dripping down her thighs. Several strong pulses hit her upper back and shoulders, some even reaching her hair.
    scene d5night255 with dissolve
    mab "Oh my god! so much!"

    # She reaches back with one hand, scooping a thick streak from her cheek and bringing it to her lips for a quick taste.
    scene d5night260 with dissolve
    mab "Oh fuck… look at it all—still coming, like you can’t stop… it’s so much, so hot…"

    scene d5night265 with dissolve
    mab "Fuck… there’s so much… you really painted me good. I love how hot it feels sliding down my skin."

    # She stays bent over, letting MC see the full mess—come dripping slowly down her curves, glistening in the dim bar lights.
    scene d5night270 with dissolve
    mab "You made a beautiful mess of me… I’m gonna remember this every time I walk past this table."
    mc "You’re incredible, Mabel. That was… intense."

    scene d5night275 with dissolve
    mab "Best private show I’ve ever given… or received. Thank you."
    mc "I have to head back to the apartment now—Rachel and Lucy are waiting for me."

    scene d5night280 with dissolve
    mab "I understand… go to them, and thank you for everything tonight."



    return


label d5apart:
    scene blackd506 with dissolve
    centered "Back at the apartment..."

    scene d5apart010 with dissolve
    mc "I’m back. Sorry I’m late."
    r "You’re here. That’s what matters. Lucy’s already asleep in her room."

    scene d5apart020 with dissolve
    r "I’m sorry, [player_name]. I keep thinking… Lucy joining us last minute changed everything. We’ve barely had a single moment alone."
    mc "It’s okay. I knew what I was signing up for."

    scene d5apart030 with dissolve
    r "No. It’s not okay. We haven’t had… us. No time to just be together. No touches. No kisses. Nothing."

    scene d5apart010_2 with dissolve
    r "Sit back… let me make you happy tonight. Just us. Finally."


    scene d5apart040 with dissolve
    r "Let me take care of you, [player_name]. Please."

    # Her fingers move to his belt, undoing it slowly, deliberately.
    scene d5apart050 with dissolve
    r "I’ve waited too long for this… let me show you how much I need you."

    scene d5apart060 with dissolve
    r "Look at me……so… what do you think? Should I keep going?"

    menu:
        "Hell yeah, keep going":
            ##show screen lust5
            $ rachel += 5
            jump rachel_tease_accept

        "Damn… tempting. But not tonight, beach goddess.":
            jump rachel_tease_reject

    return

label rachel_tease_reject:
    scene d5apart_reject010 with dissolve
    mc "You're killing me here, Rachel… but let's save the fireworks for another night."
    r "Yeah, fair. I spent the whole week treating you like a friend instead of a boyfriend. My bad."
    scene d5apart_reject015 with dissolve
    r "You’re too nice about this. I’m gonna go hide under the covers and die of embarrassment now."
    mc "We’re still good, Rachel. Promise."

    scene d5apart_reject020 with dissolve
    r "Forgive me? And… maybe give me another shot soon? When I’m not being a total disaster? Night, beach boy."

    scene blackd406 with dissolve
    centered "End of Day 5"


    call day6 from _call_day6_1
    return


label rachel_tease_accept:
    mc "Rachel… they’re… incredible. Keep going. Don't you dare stop now."

    scene d5apart070 with dissolve
    r "All for you. No more hiding. Just us."


    scene d5apart080 with dissolve
    r "Let me make you feel good… let me taste you."

    # Her fingers undo his pants, pulling them down just enough. His hard cock springs free.
    scene d5apart085 with dissolve
    r "God… you’re so hard already…I’ve wanted this cock in my mouth for days… let me worship it."


    #r "Mmm…"


    scene d5apart090 with dissolve
    r "Mmm… you’re so thick… I can barely fit you."
    mc "Fuck, Rachel… your mouth is heaven."

    #r "(popping off again, gasping, strings of spit connecting her lips to his cock) I love tasting you… love feeling you throb on my tongue."

    scene d5apart095 with dissolve
    r "gluck-gluck-gluck… mmmph…"
    mc "I’m close—Rachel—"

    scene d5apart100 with dissolve
    r "Cum for me… "

    scene d5apart105 with dissolve
    mc "Fuck...Rachel...now!"

    # MC’s cock pulses hard. Thick, heavy ropes erupt—first shot hitting the back of her throat, then she pulls off just in time.

    # The next powerful jets splash across her face—hot streaks landing on her cheeks, lips, chin—then more across her huge fake tits, dripping down the curves and between her cleavage.
    scene d5apart110 with dissolve
    r "Oh my god..so much!"

    # She keeps stroking him through it, milking every last spurt. Come drips from her chin onto her breasts, coating her nipples and running in rivulets down her stomach.
    scene d5apart115 with dissolve
    r "I… I didn’t expect this much… it’s everywhere… all over my face, my tits…"

    # She looks up at MC, face and chest glistening, a mix of shock and aroused awe in her eyes.
    scene d5apart120 with dissolve
    r "You really… filled me up. Look at me… I’m covered in you."
    l "{i}Fuck… yes…{/i}"

    scene d5apart125 with dissolve
    r "Did I make you happy?"
    mc "More than happy."

    scene d5apart130 with dissolve
    r "I’m going to go clean up this mess you made on me… I’ll be right back."
    mc "I’ll head to bed and wait for you there… don’t take too long."

    scene blackd406 with dissolve
    centered "End of Day 5"
    call day6 from _call_day6_2
    return

################### DAY 4 #################################
label morning4:
    play music musica5 loop
    scene d4apart010 with dissolve
    r "Good morning, sleepyhead."
    l "Morning, handsome! Took you long enough."
    mc "Morning, ladies. What’s the secret meeting about?"

    scene d4apart020 with dissolve
    r "No secret. Just… dealing with the consequences of last night’s card game."
    l "Yep! Mom lost big time, so today I get to pick her a brand-new bikini. Something way hotter than her usual grandma one-pieces."


    scene d4apart050 with dissolve
    r "Lucy, please. It’s embarrassing enough without the commentary."
    l "Embarrassing? Mom, you’ve got an killer body. Time to show it off. I’m thinking tiny triangles, maybe some strings… something that screams ‘sexy MILF on vacation’."


    scene d4apart061 with dissolve
    r "I knew I should never have agreed to that bet. I’m a grown woman, not some… some college girl."
    l "Exactly! Grown women can be hot. Trust me, [player_name]’s gonna love it."
    mc "Sounds like I’m in for a treat this afternoon."


    scene d4apart075 with dissolve
    r "You’re not helping."

    scene d4apart080 with dissolve
    l "Anyway, we’re heading to the shops right after breakfast. You’ve got the whole morning free, [player_name]. Maybe go for a walk… or just picture what Mom’s gonna look like later."


    scene d4apart085 with dissolve
    r "Alright, enough teasing. Let’s get this over with before I change my mind."
    l "No backing out! Come on, Mom—this is gonna be fun."


    scene d4apart088 with dissolve
    r "We’ll be back by lunch. Try not to enjoy your freedom too much."
    mc "Have fun, you two."


    scene door with dissolve
    mc "{i}Morning’s mine… Crystal’s probably opening the ice-cream parlor soon, or Alina might be free.{/i}"

    scene d4choice with dissolve
    menu morning_choice:
        "Spend the morning with Crystal (Futa content)":
            #mc "Crystal owes me a rematch… and maybe more ice cream."
            # Jump to Crystal morning scene
            jump crystal_out

        "Spend the morning with Alina":
            #mc "Alina’s smile has been on my mind since the sauna. Time to see her again."
            # Jump to Alina morning scene
            jump alina_out


    return



label afternoon4:

    scene blackd04010 with dissolve
    centered "You join Lucy and Rachel on the beach to see the bikini Lucy picked out for Rachel."

    scene d4tanlines010 with dissolve
    l "So, [player_name], what do you think Mom’s surprise is gonna look like? I went all out picking it."
    mc "Knowing you, Lucy, it’s probably the tiniest thing the shop had."

    scene d4tanlines012 with dissolve
    r "Don’t encourage her! I’m already regretting that stupid bet. I thought I had that last hand locked."
    l "Nope! You went all-in with a pair of eights. Rookie mistake, Mom. Now you get to rock my masterpiece."
    mc "I’m curious. You’ve been hyping it for hours."

    scene d4tanlines016 with dissolve
    r "Hours of dread, you mean. Lucy made me try it on and I nearly had a heart attack in the mirror."
    l "Oh come on, you looked fire! Your body is killer—why hide it? And since we found that private spot, no one else gets to enjoy it but us."

    scene dtan365 with dissolve
    l "Ready for the big reveal?"

    scene d4tanlines014 with dissolve
    r "Okay… fine. A bet’s a bet."

    scene dtan360 with dissolve
    l "Yes! Drop the cover-up, Mom! Let’s see it!"

    scene d4tanlines100 with dissolve
    l"Oh my GOD, Mom! You look insane! Those strings are basically dental floss!"

    scene d4tanlines030 with dissolve
    r "It’s… it’s obscene. I feel completely naked."

    l "That’s the point! Look at you—total MILF goals. [player_name], tell her!"

    mc "Rachel… you look breathtaking. That thing was made to show you off."

    scene d4tanlines040 with dissolve
    r "Really? Even compared to Lucy’s little number?"

    scene d4tanlines060 with dissolve
    l "Look at that, [player_name]! Every curve on display. Now the back—Mom, spin!"

    scene d4tanlines070 with dissolve
    l "Perfect, right? That string just vanishes. Mom, you’re a total bombshell!"
    r "Lucy, stop! I feel so exposed…"
    l "You’re gorgeous, Mom. Own it."

    scene d4tanlines051 with dissolve
    l "I’m proud of you for doing this. You look amazing. [player_name] can’t take his eyes off you."
    mc "She’s right, Rachel. You’re stunning. Front, back, and everything in between."

    scene d4tanlines107 with dissolve
    r "Oh, don't you start, [player_name]! I can feel every single grain of sand on my backside, and I’m pretty sure the sun is hitting places that haven't seen light since the nineties! This is a nightmare."

    scene d4tanlines108 with dissolve
    l "Mom, stop. You look hot! Seriously."
    r "Just... leave me here. Maybe I can dig a hole and bury myself until the sun goes down."
    l "Oh, come on, don't be a drama queen."

    scene dtan155 with dissolve
    mab "Well, well. Look what the tide washed up! Or should I say... look what it didn't wash up?"
    r "Oh, for God's sake. Not now, Mabel."

    scene dtan175 with dissolve
    mab "Rachel! My, my... what an ensemble. Quite the leap from yesterday, isn’t it? Weren’t you just lecturing the girls about being topless?"
    scene d4tan215 with dissolve
    r "It was a bet, Mabel! A horrible, rigged bet. Lucy’s punishing me. I’m not wearing this by choice—I’m wearing it because I have no dignity left!"
    mab "Darling, you look stunning. Honestly, this look is so much better for you. It really... accentuates your best features."
    scene dtan190 with dissolve
    mab "I mean, you’re basically naked anyway, Rachel! It’s just a few strategically placed threads. Isn’t it liberating? Think of the tan lines—or lack thereof!"

    scene dtan193 with dissolve
    r "Yes, Mabel. It’s thrilling. I can feel every breeze. It’s like I’m wearing a whisper and a prayer."

    #mab "Now, don't be a gloomy Gus! This is a fashion opportunity!"
    scene dtan194 with dissolve #196?
    mab "You know, Rachel, that little... number... is actually a similar cut to my monokini. Just with less fabric. And Sara’s bikini is such a classic."

    scene dtan195 with dissolve
    l "Wait, I have a great idea! Hey—Mabel, can we take a group pic? All the girls together?"


    scene dtan197 with dissolve
    r "A photo? Lucy, no. Absolutely not. I am not letting there be photographic evidence of this humiliation. Especially not while I'm wearing... this."
    #r "Are you out of your mind, Lucy?! Absolutely not! Mabel, don't you dare give her that look."

    scene dtan200 with dissolve
    mab "Oh, don't be such a prude, Rachel! It’s just a bit of fun. A little beach-side fashion show!"


    scene dtan202 with dissolve
    r "Wait—wait, no. A photo? Like this? I… I don't think so."
    l "Mom, come onnn. It's just us. No one else will see it. It's our little secret souvenir."


    scene d4tan215_2 with dissolve
    r "It's not just that. I already feel ridiculous in this… thing. Having a picture of me like this? What if someone finds it? What if—"
    mab "Rachel, sweetheart, listen to me. You are not ridiculous. You are breathtaking. That slingshot looks like it was made for you. And this photo? It's proof of how brave you were today."

    scene dtan350 with dissolve
    l "Mom… you've been amazing all afternoon. You walked out here, you let Mabel see you. This is just one more little step."
    mab "Exactly. One photo. Three women feeling good in their skin. No judgment, no sharing, just us."


    scene dtan370 with dissolve
    r "I… I don't know…"
    l "Please? For me? And for you. You'll look back one day and be proud of this moment."

    scene dtan322 with dissolve
    mab " And if you hate it after we take it, we delete it. No pressure. But I think… you'll love it."
    r "…Fine. One photo. But only one. And if I look awful, we erase it immediately."
    scene dtan380 with dissolve

    l "Yes! You're the best mom ever!"

    scene dtan327 with dissolve
    mab "That's the spirit. Come here, gorgeous."
    scene dtan300 with dissolve
    l "Perfect! Mom in the middle—show off that slingshot! Mabel on one side, me on the other. [player_name], you’re our photographer!"
    mc "Ready when you are."


    scene dtan305 with dissolve
    l "Smile, Mom! Show the world what a hot mom looks like!"
    r "You’re impossible…"
    mab "Relax, gorgeous. You’re stunning."


    scene dtan370_2 with dissolve
    l "Wait—one more! Quick ass pics! Super fun, super fast!"
    r "No. Absolutely not. The front was already too much."


    scene dtan355 with dissolve
    l "Please, Mom? Just one shot, no face. Done in ten seconds. Then we’re finished."
    r "…Fine. Only one. Fast. Then we’re done. I want to get this over with."


    scene dtan310 with dissolve
    l "Yes! Mom in the middle, tiny arch!"


    scene dtan315 with dissolve
    mab "Like this, Rachel. Quick and easy."
    l "Perfect! [player_name], snap!"



    scene dtan320 with dissolve
    mab "Well, darlings, that was a shoot to remember! I think we really captured the spirit of... spontaneous liberation."

    scene dtan325 with dissolve ##o stan327
    l "It was a blast, Mabel."


    scene dtan330 with dissolve
    mab "It really was! But duty calls. Sara and I have a few things to run before tonight. We’ll have to say goodbye for now."


    scene dtan340 with dissolve
    r "Oh, thank God. Finally. I don't think my heart can take any more 'liberation' for one day."


    scene dtan345 with dissolve
    mab "It was a pleasure, Lucy!"
    l "We really have to do this again soon..."

    scene d4tan225 with dissolve
    mc "So, what’s the move for tonight? More sand, or are we heading out?"
    l "Oh! Can we go back to the show bar? George said Claudia would be performing again! Maybe Mabel will show up too!"
    r "The show bar? No. Absolutely not, Lucy. Not after last night. That place is a den of... well, it's questionable. And that Claudia woman? Absolutely not."

    scene d4tanlines020 with dissolve
    l "Please, Mom! I promise I'll be good. I really want to see Claudia’s set again!"

    scene dtan375 with dissolve #dtan377 379
    mc "Oh, come on, Rachel. It wasn't that bad. It's just a show... it’s a vacation. Live a little."
    r "Ugh, you two are impossible. Fine! But we are NOT sitting in the front row again!"

    scene dtan380 with dissolve
    l "Yes! Thank you, Mom! You're the best!"
    mc "Perfect. Let’s get cleaned up then. The bar is calling."

    #jump night4

    return

label night4:

    scene d4barwelcome with dissolve
    ge "Welcome back, [player_name], Rachel, Lucy! Got the best table for you as always"

    scene d4base012 with dissolve
    r "Oh, great. Front row for… whatever this is going to be."
    l "Relax, Mom. It’s just a show."
    mc "You two grab the table—I’ll get the first round of beers."


    scene d4base060 with dissolve
    menu peek_choice:
        "Sneak a quick peek at the woman’s cleavage":
            scene d4base065 with dissolve
            pause 2.0

            scene d4base075 with dissolve
            u "Like what you see, handsome?"

            scene d4base070 with dissolve #076
            u "Don’t be shy—enjoy the view."


            scene dbase080 with dissolve
            u "If you’re still thirsty after those beers, come find me later."

            scene d4base095 with dissolve
            sar "Hey, [player_name]. Beers for the table? Three, right? Coming up."

            #reduir lust sara

            #show screen lustm5
            $sara -=5

            scene d4base107 with dissolve
            sar "You know, some of us don’t need {b}that{/b} much to get attention."
            mc "Sorry, Sara. Just got distracted for a second."


            jump bar_continue


        "Keep eyes on Sara and ignore the departing woman":

            scene d4base100 with dissolve
            sar "[player_name]! Perfect timing—I was hoping you’d come say hi."

            scene d4base110 with dissolve
            sar "Three beers for you and the ladies? Or did you just come to see me?"
            mc "A bit of both. You’re looking great tonight, Sara."

            scene d4base105 with dissolve
            sar "Smooth talker. Beers are on the house."
            mc "Thanks"

            scene dbase120 with dissolve
            sar "How about I bring these to your table myself? That way I get to say hi to Rachel and Lucy… and maybe steal a minute with you."
            mc "Sure"
            jump bar_continue

    return

label bar_continue:

    scene d4base120 with dissolve
    sar "Here we are—three cold ones, just like you ordered!"
    r "Thanks."
    l " Sara! You’re a lifesaver!"


    scene d4base127 with dissolve
    sar "Everything okay, [player_name]? You look a little… distracted."
    mc "Yeah, everything’s perfect. Thanks again for the drinks."
    scene d4base125 with dissolve
    sar "Good. Enjoy the show. I’ll swing by later if I get a break."


    scene d4base140 with dissolve
    mab "Good evening, darlings! Welcome to the hottest spot in town! Tonight, our star, Claudia, has a special treat. Her outfit? Inspired by a stunning woman in our audience!"

    scene d4baseworr01 with dissolve
    r "Oh no. No, no, no. She better not mean—"
    mc "What's wrong, Rachel?"
    scene d4baseworr02 with dissolve
    r "She's... she's looking at me! I just know it!"

    scene d4base145 with dissolve
    mab "Without further ado, let's welcome the sensational, the seductive, the simply scandalous Claudia!"

    # "Mabel backs away, a wicked twinkle in her eye, as the red velvet curtains part with a dramatic flourish."

    # "And there she is. Claudia. But this time, she's not in pasties and a thong. Instead, she's wearing... a slingshot? And holding two massive, feathered fans that shimmer like fallen clouds."

    play music musica6 loop
    scene 4dfan020 with dissolve
    c "Good evening, everyone! Hope you're ready for a little whirlwind!"

    scene d4fan050 with dissolve
    r "That’s… that’s like my slingshot swimsuit! She’s mocking me! [player_name], tell me you’re not staring!"

    scene d4fan111 with dissolve
    mc "Uh, just… appreciating the artistry."
    scene d4fan116 with dissolve
    l "Oh, come on, Mom, it’s hot! Claudia’s killing it. Bet I could pull that off too, [player_name]. Wanna see me try later?"
    scene d4base170 with dissolve
    r "Lucy! Behave yourself!"

    scene d4base165 with dissolve
    r "I’m going to die. Right here. In this chair."

    scene 4dfan026 with dissolve
    r "Oh, my word. She's... she's wearing nothing but that little thing!"
    scene d4fan027 with dissolve
    l "Whoa! Mom, that's almost what you wore to the beach today!"
    r "Lucy, shush!"

    scene d4fan060 with dissolve
    l "She's so... confident. And hot. Like, seriously hot."

    scene d4fan118 with dissolve
    r "I can't believe this!"
    scene d4fan119 with dissolve
    pause 2.0
    scene d4fan122 with dissolve
    r "She's completely naked under those fans!"
    scene d4fan040 with dissolve
    mc "It's certainly... a bold choice."

    scene d4fan032 with dissolve
    l "I mean, if you got it, flaunt it, right? And she definitely has it."


    scene d4base175 with dissolve
    r "I'm going to melt into the floor."
    mc "Well, at least you know you have good taste, Rachel. Imitation is the sincerest form of flattery, after all."

    stop music fadeout 1.0
    play sound "Applause.mp3"

    scene d4base172 with dissolve
    l "Oh my god, Mom—Claudia’s show was insane! I’m still shaking from how hot that was!"
    r "Thank goodness it’s over… I don’t think my heart could take another minute of that intensity."


    scene d4basend010 with dissolve
    sar "Can I get you anything else? Perhaps something to cool you down?"
    mc "I think we might need a whole ice bath after that."

    scene d4basend020 with dissolve
    sar "She certainly knows how to put on a show."
    r "Understatement of the year."

    scene d4basend030 with dissolve
    l "She's amazing! Don't you think she's amazing, [player_name]?"
    mc "She's... memorable, Lucy. Very memorable."

    scene blackd406 with dissolve
    centered "End of Day 4"

    jump day5
    return


label crystal_out:

    scene icecreamshop02_c4 with dissolve
    mc "Morning, Crystal. Slow day?"
    cryst "Hey, [player_name]! Yeah, just the usual pre-lunch lull. What brings you in?"

    scene icecreamshop04_c4 with dissolve
    mc "Actually... I was thinking of inviting you out. You deserve a break. Come out with me—let’s do something fun."
    cryst "A break? Hmm… I do have a slow hour coming up. How about we play tennis? There’s a public court two blocks over—no crowds, just us."

    scene icecreamshop012 with dissolve
    mc "Good enough to lose gracefully if you’re serving."
    cryst "Deal. Give me two minutes to flip the sign to ‘Back in 60’ and change."


    scene icecreamshop016 with dissolve
    cryst "Uniform off, game on. Ready to get sweaty?"
    mc "More than ready."

    scene icecreamshop018 with dissolve
    cryst "Best of three sets, [player_name]. Loser buys the ice cream—deal?"
    mc "Best of three it is. I’m buying either way—just want to enjoy the show."

    #mc "Let’s go, Crystal. Winner takes all… and the loser takes the bill."


    #cryst "Well? You coming, or are you just gonna stare?"

    #mc "You look incredible."

    #cryst "Flattery won’t save you on the court, sugar."


    scene tennis010 with dissolve
    mc "Your serve, Crystal."
    cryst "Ready to get schooled? Or should I say… distracted?"

    scene tennis015 with dissolve
    cryst "Try to keep up!"
    mc "Let’s see what you’ve got. But with that outfit, you’re already winning."


    scene tennis025 with dissolve
    cryst "These girls are just so bouncy when I swing hard—can’t help it!"
    mc "You’re making it impossible to keep my eyes on the ball."

    scene tennis030 with dissolve
    cryst "Got it—stay down for this one! Did my boobies get in the way again? They always want to say hello!"
    mc "Yeah… and I didn’t even see the ball coming."

    scene tennis020 with dissolve
    cryst "Come on, [player_name], serve already! I'll be right here… trying to keep everything in place!"
    mc "That’s the problem…"

    scene tennis035 with dissolve
    cryst "Up we go—whee! Wow, they really flew that time! Hope they didn’t distract you too much~"

    scene tennis040 with dissolve
    cryst "Game, set, match! Two-one."

    scene tennis055 with dissolve
    mc "I’m hitting the changing room."
    cryst "Don’t take too long, loser."

    scene d4lock010 with dissolve
    cryst "Oops… wrong door? Or maybe the {b}right{/b} one."
    mc "Crystal… this is the guys’ side."

    scene d4lock040 with dissolve
    cryst "Like that ever stopped me."

    scene d4lock045 with dissolve
    cryst "I’m still buzzing from that win, [player_name]. I need you inside me. Right here. Right now."

    scene d4lock050 with dissolve
    cryst "Fuck me. Hard. Make me feel every point I earned."

    menu:
                "Accept Crystal":
                    jump accept_crystal
                "Refuse Crystal":
                    mc "Crystal… wait. You were incredible out there, and you’re gorgeous. Really. But… I can’t."


                    scene d4lock_reject with dissolve
                    cryst "…Oh. You’re serious?"
                    mc "Yeah. I’m sorry. It’s not that I don’t want to—I do. You’re fucking hot. But I need to head back soon. Rachel and Lucy are waiting."

                    scene d4lock_reject02 with dissolve
                    cryst "Fair enough, handsome. A girl can try. Maybe next time then. When you’ve got a free morning… or a free night. I’ll be waiting to lose—or win—another match."
                    mc "Count on it. Next time, I might not be so polite."

    return

label accept_crystal:

    scene d4lock055 with dissolve
    mc "You don’t play fair…"
    cryst "Who said anything about fair? Take me, champ."

    $crystal += 10
    $lust += 10
    #show screen lust10

    scene d4lock052 with dissolve
    #cryst "You really thought you could just shower and leave me hanging after that match?"

    cryst "Every time I bent over… every time my skirt flipped… I was thinking about your cock."

    mc "Crystal…"

    #cryst "(pressing her body against his back, cock sliding along his thigh) Mmm, feel that? That’s what you do to me."

    # She reaches around, palming him through the boxers.

    cryst "Already so hard again. Good boy."

    # She tugs the boxers down, letting them pool at his feet. His cock springs free.

    scene d4lock060 with dissolve
    cryst "Mmm, look at this racket. Been dying to wrap my mouth around it since set two."

    # Crystal drops gracefully to her knees in front of him, breasts bouncing softly as she settles.


    scene d4lock070 with dissolve
    cryst "There it is… my favorite trophy. Time to claim my real prize. Mmmm..."
    mc "Jesus, Crystal… your mouth is filthy."

    scene d4lock075 with dissolve
    cryst "Taste how much I wanted this? I love this cock…"
    mc "Fuck, Crystal…"


    scene d4lock080 with dissolve
    cryst "Mmmph...so good..."



    scene d4lock085 with dissolve
    cryst "But I’m not done. Turn me around. I want you inside me..."

    scene d4lock095 with dissolve
    cryst "Yes! Stretch me, [player_name]. Make me feel every point I won."
    mc "You’re so tight… like you’re milking me."

    scene d4lock105 with dissolve
    cryst "Harder! Fuck me like you mean it! I want to scream!"
    mc "Crystal—fuck—!"


    scene d4lock110 with dissolve
    cryst "Mmm… that’s how you pay a debt."


    scene d4lock115 with dissolve
    cryst "Yes! Fuck me just like that, [player_name]! Deeper, harder!"
    mc "You feel so fucking good, Crystal…"

    scene d4lock120 with dissolve
    cryst "Look at me...watch me stroke this cock for you…"

    scene d4lock125 with dissolve
    cryst "I’m close...fuck...gonna come all over myself!"
    mc "Do it. Cum for me."

    scene dlock130 with dissolve
    cryst "Yes—yes—OH FUCK!"


    scene dlock147 with dissolve
    cryst "Mmm… your turn, baby. Pull out… cum on me. Paint my tits, my face...mark me."

    scene dlock148 with dissolve #era 145
    mc "Crystal...shit..."

    scene dlock150 with dissolve
    cryst "Do it—give me every drop. I want to feel you hot on my skin…"

    scene dlock153 with dissolve  #o 154 o 156
    cryst "Yes! So warm… so much…Perfect ending to a perfect match."
    mc "You’re going to kill me one of these days."

    scene dlock157 with dissolve
    cryst "Only if you keep losing on purpose."

    scene dlock155 with dissolve
    cryst "Look at this mess we made. Let me clean you up… properly."


    scene dlock160 with dissolve
    mc "Crystal… fuck, your mouth again?"
    cryst "Mmmph—can’t get enough."


    scene dlock165 with dissolve
    cryst "I want every drop."

    scene d4lock110 with dissolve
    mc "You’re insatiable."
    cryst "Only for you, champ."


    scene dlock170 with dissolve
    cryst "Mmm… best match I’ve ever played."
    mc "Same. You’re a champion."

    #172 & 174
    scene dlock174 with dissolve
    mc "See you, Crystal."
    cryst "Count on it, handsome."



    return

label alina_out:

    scene alina_cell010 with dissolve
    w "Hey, [player_name]. Perfect timing."
    mc "Hey, beautiful. Got plans today?"

    scene alina_cell020 with dissolve
    w "Actually… I was about to head to the sauna. Quiet, steamy, very relaxing. Want to join me?"
    mc "I’m already grabbing my keys."

    w "Good. I’ll text the address. See you in twenty."

    # Scene: Private Sauna – Evening
    # Steam curls thick and fragrant; cedar walls glow amber under soft lights.


    scene d4sauna010 with dissolve
    w "I thought we’d have the place to ourselves…"

    scene d4sauna015_d with dissolve
    da " Hello there. Don’t worry, there’s plenty of room. I’m Dana. I come here whenever I need to unwind. And you two?"
    mc "I’m [player_name]. This is Alina."
    w "Nice to meet you, Dana."

    scene d4sauna025 with dissolve
    da "Pleasure’s all mine. This heat is heaven, isn’t it? Loosens everything up."
    mc "Definitely. It’s our first time at this place."
    da "First time in a sauna like this? You’ll get addicted. Especially with the right company."

    scene d4sauna035 with dissolve
    w "We were hoping for a quiet morning..."

    scene d4sauna045 with dissolve
    da "Oh, I understand completely. Young love needs space."

    scene d4sauna065 with dissolve
    da "Though if you ever want tips on the best temperature settings, [player_name], I’m happy to share my secrets."
    mc "I’ll keep that in mind."
    scene d4sauna055 with dissolve
    w "We’ll manage, thanks."

    scene d4sauna085 with dissolve
    da "Well, I should head out. You two enjoy the rest of your day."
    scene d4sauna090 with dissolve
    da "Hope to run into you again sometime."

    scene d4sauna095 with dissolve
    w "She was… very comfortable."
    mc "You okay?"

    scene d4sauna100 with dissolve
    w "[player_name]… be honest with me, please. Did you… like her? Dana, I mean. She was so confident, so beautiful… I saw how you looked at her. Just tell me the truth."

    menu sauna_jealousy_choice:
        "Tell Alina you found Dana attractive":
            mc "She was… yeah, pretty stunning. Hard not to notice."

            scene d4sauna105 with dissolve
            w "I thought so. It’s okay… I understand."

            scene d4sauna106 with dissolve
            w "I think I need some air. Enjoy the rest of the sauna."

            jump afternoon4

        "Reassure Alina that you only want her":
            mc "She? She’s nothing compared to you, Alina."
            scene d4sauna110 with dissolve
            mc "I didn’t come here for anyone else. I came for you. You’re the one I can’t stop thinking about."

            scene d4sauna115 with dissolve
            w "(eyes softening, a shy smile) Really…? You mean that?"
            mc "Every word."


            scene d4sauna120 with dissolve
            w "Then show me…I want to feel like the only woman in the world for you tonight."

            jump sauna_intimate

    return

label sauna_intimate:

    $alina += 5
    $lust += 10
    #show screen lust10

    scene d4sauna136 with dissolve
    w "I need to taste you first…"

    scene d4sauna140 with dissolve
    w "You’re already so hard for me…"

    # She leans in, tongue flicking the tip—*slurp*—then takes him slow and deep, lips sealing tight.
    scene d4sauna145 with dissolve
    w "Mmm…"
    mc "Alina… your mouth feels incredible."

    scene d4sauna150 with dissolve
    w "Mmmph...so thick…"
    mc "Fuck, Alina… your throat is insane...taking me like that…"
    # She strokes him with one hand, sucking harder—*gluck, slurp*—until MC’s hips twitch.


    scene d4sauna155 with dissolve
    w "I love how you taste…"
    mc "I need you now."

    scene d4sauna160 with dissolve
    w "Oh… yes… so deep…"
    mc "You’re so tight… so perfect."

    scene d4sauna165 with dissolve
    w "Harder… please…"

    # MC thrusts up to meet her, skin slapping wetly—*slap, slap*—her cries echoing in the steam.

    scene d4sauna170 with dissolve
    w "I’m close...don’t stop! AHHHHH!"

    scene d4sauna175 with dissolve
    w "Your turn… from behind. Take me like this… I want to feel all of you."
    mc "Fuck, Alina…"


    scene d4sauna176 with dissolve
    w "Yes!I’m so close again!"
    mc "Alina… Fuck! I’m gonna come—"

    scene d4sauna180 with dissolve
    w "Pull out...please...come on my back… paint me…"

    scene d4sauna185 with dissolve
    mc "Now!"

    scene d4sauna190 with dissolve
    w "Mmm… so warm… I can feel every drop…"

    scene d4sauna195 with dissolve
    w "Look what you did to me… your come all over my back… do you like your artwork?"
    mc "You look… fucking incredible like that."


    scene d4sauna200 with dissolve
    w "Mmm, it’s sliding down… feels so dirty and perfect…"



    scene d4sauna210 with dissolve
    w "Now let me clean you up… every last bit."


    scene d4sauna215 with dissolve
    w "Mmm… we taste amazing together."


    scene d4sauna230 with dissolve
    w "All clean… for now."
    mc "You’re going to be the end of me."


    scene d4sauna225 with dissolve
    w "I could stay like this forever…"
    mc "Me too. But… I really have to head back. Rachel and Lucy are waiting for me on the beach."

    scene d4sauna205 with dissolve
    w "Thank you for today, [player_name]. For choosing me."
    mc "Always. See you soon?"

    scene d4sauna235 with dissolve
    w "Count on it. Go—before I change my mind and lock the door."
    mc "Tempting… but duty calls. Goodbye, Alina."

    return



################### DAY 3 #################################
label topless:

    play music musica5 loop

    scene black02 with dissolve
    scene black03 with dissolve

    centered "On the morning of the third day, you all decide to head back to the beach together, returning to your little slice of paradise, the same secluded spot you claimed yesterday."



    scene d3beach011 with dissolve
    r "I still can't believe you wore that, Lucy! It's practically nothing!"
    l "Mom, chill! It's just a bikini. Everyone wears these now. It's totally modern."

    #scene d3beach020 with dissolve

    scene d3beach012 with dissolve
    r "Modern? It's scandalous! You're barely covered!"
    l "Exactly! It's called confidence. Besides, who's even here? It's not like we're in a crowded resort."
    mc "She's not wrong. We really did pick a deserted spot."
    r "Still! What if someone walks by? Or a boat? Honestly, Lucy."

    scene d3beach030 with dissolve
    l "Mom, you're so dramatic. No one's going to care."
    r "Fine, fine! I give up."
    scene d3beach040 with dissolve
    r "Hey, [player_name], could you do me a favor? My back is starting to feel a bit tight from the sun. Could you put some sunscreen on for me?"
    scene d3beach060 with dissolve
    mc "No problem, Rachel. "
    scene d3beach070 with dissolve
    mc "{i}Looks like Lucy is in her own little world, as usual.{/i}"
    scene d3beach090 with dissolve
    r "Ah, that's much better, [player_name]. Thanks, you're the best."
    scene d3beach130 with dissolve
    r "Why we don't..."
    scene d3beach110 with dissolve
    r "LUCY! WHAT ARE YOU DOING?!"
    scene d3beach100 with dissolve
    l "Ugh, Mom! What now?"
    scene d3beach140 with dissolve
    r "What now?! You're TOPLESS! On a public beach! What were you thinking?!"
    l "There's NO ONE HERE! And I'm just taking some pictures for my friends!"
    scene d3beach150 with dissolve
    r "I don't care! It's completely inappropriate! Put your top back on, right now!"
    l "God, you're such a buzzkill! This is why I can't stand coming on holidays with you!"
    scene d3beach170 with dissolve
    r "Don't you dare talk to me like that! I'm your mother!"
    l "I'm going for a walk! Don't follow me!"
    scene d3beach180 with dissolve
    r "And for heaven's sake, if you're going to leave, put your top back on at least! Have some decency!"
    scene d3beach190 with dissolve
    l "Fine! Just to get you to stop yelling!"
    r "Honestly, I'm done with her."
    mc "{i}Well, that escalated quickly. As always.{/i}"
    scene d3beach200 with dissolve
    mc "Rachel, maybe I should go after her. Talk some sense into her."
    r "Hmph. As if she'll listen to you, [player_name]. She never listens to me."
    mc "It's worth a shot. She's upset. Someone should go."
    scene d3beach210 with dissolve
    r "Fine. But if she gives you any grief..."
    mc "Don't worry. I'll handle it."

    ######

    scene d3beach230 with dissolve
    mc "Lucy! Hey, Lucy, wait up!"
    scene d3beach240 with dissolve
    l "What do you want, [player_name]? Mom send you to lecture me?"
    mc "No, no. Not at all. I just... wanted to see if you're okay. And talk."
    scene d3beach250 with dissolve
    l "I'm fine. Just fed up. She's always like this. Always has to control everything."
    mc "She's just worried about you, you know. It comes from a place of... well, a mother's instinct."
    scene d3beach260 with dissolve
    l "Worried? She's suffocating! I'm not a little kid anymore! I can make my own choices about what I wear, or... or anything!"
    mc "{i}She's got a point. Rachel can be a bit too much sometimes.{/i}"
    scene d3beach270 with dissolve
    l "And seriously, a bikini? What's the big deal? It's just skin! It's natural! And it's for my friends, not for creepy old men on the beach!"
    mc "I know, I know. Look, she'll calm down. It's a holiday, no need for all this tension."
    l "Easy for you to say. You don't have to live with her trying to dictate your every move."
    scene d3beach280 with dissolve
    mc "Hey. Come on. Don't let it ruin your day. This is our holiday. Let's just try to enjoy it, okay?"
    l "I guess..."
    scene d3beach310 with dissolve
    mc "That's better. Now, what were those pictures for, anyway? Just for friends?"
    l "Well, actually... not {b}just{/b} for friends. I have this online account, you know? For, like, my fans."
    mc "Fans? "
    scene d3beach320 with dissolve
    l "It's for my adult content. Nothing too wild, yet. But I want to build it up. And... well, you're pretty good with a camera, aren't you?"
    mc "I dabble."
    scene d3beach340 with dissolve
    l "So... I was thinking. Since you're here, and you're not, like, some pervy old dude... would you mind taking some really special pictures for me? For my account?"
    mc "Special pictures, huh? Rachel would freak. Alright, Lucy. If you're sure about this. What kind of 'special' pictures are we talking about?"
    scene d3beach350 with dissolve
    l "Yes! I knew you'd be cool! Nothing too crazy, just... hotter. You know, really capture the moment. Really show off the curves. Here's my phone. Just... try to make them look good, okay?"
    l "I'll start with just topless, to ease into it. But be warned... I'm going to get much bolder."
    mc "Sounds good to me. Take your time."
    scene d3beach410 with dissolve
    l "Alright, [player_name]. Get this. Make it amazing. This is for my fans... and maybe for me, too."
    scene d3beach350 with dissolve
    mc "Hey, Lucy? Could you face the sea for a moment? I want to get a shot of your back and, uh... your ass, with the waves in the background."
    scene d3beach400 with dissolve
    l "Oh! Sure. Like this?"
    mc "Now, Lucy... show me what you've got."
    scene d3beach410 with dissolve
    l "Oh, you want me to {b}really{/b} show you, huh?"
    mc "Tease the camera. Tease me."
    scene d3beach500 with dissolve
    l "Heh. My pleasure."
    mc "Think about all those fans and followers who are going to go wild for this."

    scene d3beach490 with dissolve
    l "Oh, I am. And I'm going to make sure they get exactly what they came for. And maybe a little extra, just for you."
    mc "Alright, Lucy, let's make this go viral."

    scene d3beach460 with dissolve
    l "Like this? Is this 'viral' enough for you, [player_name]?"
    mc "Oh, Lucy, that’s more than viral. It’s just great!"


    scene d3beach510 with dissolve
    l "Alright, [player_name], ready for the grand reveal? These bottoms are about to come off..."

    scene d3beach530 with dissolve
    sar "Oh! [player_name]? What’s going on here?"
    scene d3beach537 with dissolve
    l "Who’s this chick? [player_name], you got a secret sidekick already?"
    mc "Sara, hey! Just… taking some photos. Lucy, this is Sara. We met yesterday."
    scene d3beach547 with dissolve
    sar "Um, hi, Lucy. Cool… tiger stripes."
    scene d3beach549 with dissolve
    l "Thanks. So, [player_name], how exactly do you know this girl? Spill it. Wait...isn't it our lovely waitress from last night!"
    sar "Y-yes... that was me. It's... nice to meet you. Properly."
    scene d3beach541 with dissolve
    l "So, Sara, don't just stand there! We're having a little photoshoot for my online adult account. You should totally join us! We could even share the pics if you want?"
    sar "Oh, no, I... I don't have... adult accounts."
    scene d3beach545 with dissolve
    l "No way! Really? You don't have one? But... almost all girls do these days. And you're so pretty and hot, Sara, you'd make a fortune!"
    sar "I... I couldn't."
    scene d3beach546 with dissolve
    mc "Come on, Sara. It could be fun. Lucy's great."
    sar "B-but... I'm not really... I don't..."
    scene d3beach548 with dissolve
    l "Relax... Look, I'll be totally nude, and you can just go topless. How about that? A little bit of daring for each of us."
    sar "Topless?"
    mc "Yeah, just topless, if you want. No pressure, but it'd be awesome."
    scene d3beach552 with dissolve
    sar "O-okay... Fine. But... just topless, like you said."
    scene d3beach544 with dissolve
    l "Excellent! That's the spirit, Sara! Now, let's get some amazing shots"
    scene d3beach543 with dissolve
    sar "Oh, like the ones [player_name] took of my mom and Alina yesterday? Those were... uh..."
    scene d3beach551 with dissolve
    l "Wait, what? [player_name], you took pics of her mom? What kind of pics?"
    mc "It was just a favor! Nothing major!"
    scene d3beach542 with dissolve
    sar "Yeah, nothing major! Just, like... artistic. You know, with no clothes or anything."
    scene d3beach644 with dissolve
    l "No clothes?! [player_name], you’re full of surprises! Okay, Sara, you’re posing with me now. Let’s make it artsy."

    scene d3beach770 with dissolve
    l "Yo, [player_name], I’m ready to slay this shoot! Let’s make these pics fire!"
    sar "Um, okay, I’ll try too… just tell me what to do."

    mc "Alright, Lucy, Sara, get closer, faces almost touching, breasts too, and face the camera. Give me something bold!"
    scene d3beach800 with dissolve
    l "Like this, [player_name]? Bet you’re loving the view!"
    sar "Lucy, you’re too much! But… this is kinda fun."

    scene d3beach810 with dissolve
    r "[player_name]! LUCY! What in God's name is going on here?!"
    mc "Rachel! I can explain! It's not what you think!"
    l "Mom! We're just doing art! Don't be such a prude!"

    scene d3beach820 with dissolve
    r "Art?! Lucy, you are naked! And who is this girl?! [player_name], what were you thinking, taking pictures?! I can't believe this!"

    scene d3beach840 with dissolve
    sar "Oh! I'm so sorry! I... I'm Sara. I just met [player_name] yesterday, and Lucy just invited me..."

    scene d3beach860 with dissolve
    r "Lucy, you’re putting on a damn show out there, and you, [player_name]! Taking pictures of my daughter like this?! And with... with a stranger!"

    scene d3beach870 with dissolve
    mab "Well, well, what do we have here? Looks like the party's just getting started."

    scene d3beach890 with dissolve ##875
    sar "Mom! Oh, thank goodness! This is Rachel, and her daughter Lucy, and ... [player_name]..."
    mab "Hello, Rachel. I'm Mabel, Sara's mother. You're looking... very free-spirited today."

    scene d3beach877 with dissolve
    mab "And [player_name], always good to see you enjoying the beach scenery. Looks like you've found some excellent subjects for your camera, as always."

    scene d3beachrachelangry
    r "Scenery? This is my daughter, Mabel! And she is {b}not{/b} a subject for 'scenery'!"

    scene d3beach889 with dissolve
    mab "Oh, of course, darling. My apologies. Just admiring the... natural beauty of the beach, that's all."

    scene d3beach888 with dissolve
    mab "Sara, my dear, perhaps you should come with me. It looks like things are getting a little... heated here."

    scene d3beach891 with dissolve
    sar "Bye, [player_name]. Bye, Lucy."

    scene d3beach896 with dissolve
    l "See ya, Sara. And thanks for the fun!"
    r "That's it. Lucy, you are coming with me. And you, [player_name], we are having a very serious talk back at the apartment. Now!"


    scene d3beach892 with dissolve
    mab "Well, [player_name]. It seems you have quite the knack for attracting... interesting situations. Don't be a stranger, though. There's always more 'artistic' inspiration to be found around here."

    return

label apart3:

    scene black04 with dissolve
    centered "You all return to the apartment."

    scene d3apart005 with dissolve
    mc "Rachel? What's wrong?"

    scene d3apart007 with dissolve
    r "Oh, don't play innocent with me! I saw you, [player_name]! With Lucy and that other girl! What in god's name were you doing taking pictures of them nude?!"
    mc "Rachel, wait! It's not like that! They were just having fun, I was trying to capture a happy moment."

    scene d3apart010 with dissolve
    r "A happy moment?! You thought it was a 'happy moment' to exploit my daughter like that?! You were taking pictures of them nude! What were you thinking?! Are you completely out of your mind?!"
    mc "No, Rachel, please! You've got it all wrong! They were just playing, and I thought it was cute. There was no harm, no malice, nothing inappropriate!"

    scene d3apart008 with dissolve
    r "Inappropriate?! I trusted you with Lucy, and you repaid that trust by turning her into a spectacle!"
    mc "I swear, Rachel, I would never do anything to harm Lucy! It was just innocent fun, they weren't... exposed. I just snapped a few pictures of them playing, as a memory."

    scene d3apart030 with dissolve
    r "Don't you dare lie to my face! I saw what I saw! And frankly, I don't care if it was 'innocent fun' or whatever twisted excuse you're cooking up! You crossed a line, [player_name]! A huge, unforgivable line!"

    scene d3apart050 with dissolve
    r "And as if that wasn't enough to ruin my entire week, I just wanted to heat up some food and try to forget this nightmare, but no, even that's too much to ask for! The microwave is broken! Just another perfect addition to this absolutely horrendous day!"
    mc "Broken? Are you sure? Maybe it's just unplugged?"

    scene d3apart020 with dissolve
    r "It's plugged in, [player_name]! I'm not a fool! It's completely dead! You know what? I can't even look at you right now. Get a new one."
    mc "A new one? Where am I supposed to get a microwave right now?"

    scene d3apart8 with dissolve
    r "Don't play dumb! George! Our landlord George lives just a few blocks away. You’d better march over to George’s house right now and get us a new one!"
    mc "Alright, alright, I’m going. I’ll talk to George and get it sorted."

    scene d3apart040 with dissolve
    r "You’d better, [player_name]. I’m not in the mood for more excuses! Get out of my sight. Go!"
    #r "Go to George's. Tell him the microwave broke – only the microwave, don't mention your disgusting behavior on the beach – and get a working one. Now. And don't come back without it."
    #mc "But Rachel, it's getting late, he might be busy..."

    #r "I don't care! Just go! Get out of my sight. Go!"
    #mc "(Sighs, defeated) Fine. I'll go to George's."

    return

label jacuzzi:
    scene black05 with dissolve
    centered "You leave the apartment and head to George's house, to ask for a new microwave."

    scene d3entrada010 with dissolve
    mc "{i} This must be the house{/i}"
    play sound "doorbell.mp3"
    ge "Coming!"

    scene d3entrada020 with dissolve
    ge "[player_name]! What a surprise! Come on in. Rachel sent you about the microwave, right?"
    mc "Hey George. Yeah, it’s busted. Rachel’s not thrilled, so here I am."

    scene d3entrada030 with dissolve
    ge "Come in, come in. Claudia's in the kitchen, probably whipping up something delicious as always. Let's go see her."
    mc "Alright."

    # Move to the kitchen
    scene d3entrada050 with dissolve
    c "Well, well, [player_name]! Didn’t expect you so soon."
    mc "Hi, Claudia. Just here about the microwave. It’s giving us trouble."

    scene d3entrada060 with dissolve
    c "That old thing? Always breaking. George, love, why don’t you head to Crestview? They’ve got the best microwaves there."
    ge "Crestview? That’s nearly an hour away!"


    scene d3entrada070 with dissolve
    c "Only the best for our guests, right, [player_name]?"
    ge "Alright, alright. I’ll go. Be back in a couple hours."


    scene d3entrada080 with dissolve
    c "So, [player_name], just you and me now. How you holding up? That argument with Rachel sounded… heated."
    mc "I’m alright, I guess. Rachel’s just frustrated. About the microwave, and… other stuff."

    scene d3entrada085 with dissolve
    c "Other stuff, huh? Like my little belly dance at the show bar last night? I saw you watching, eyes all hungry."
    mc "Yeah, it was… something else. I enjoyed it. Lucy did too, thought it was awesome. Rachel, though… she wasn’t impressed. Stormed out, actually."

    scene d3entrada090 with dissolve
    c "Rachel’s missing out. My dancing’s not for prudes. But you, [player_name], you get it."
    mc "You dancing again tonight? I’d like to see more."


    scene d3entrada075 with dissolve
    c "Not tonight, darling. Tomorrow. I’m planning something… unforgettable. Maybe you’ll give me some inspiration."

    scene d3entrada100 with dissolve
    c "Speaking of unforgettable… how about a dip in the jacuzzi out back? It’s private, perfect for relaxing."
    mc "Jacuzzi sounds great, but… I didn’t bring any swim trunks."

    scene d3jacuzzi020 with dissolve
    c "Swim trunks? Oh, darling, I don’t bother with those either."

    scene d3jacuzzi040 with dissolve
    c "Come on, [player_name]. Let’s both get comfortable. Join me in the jacuzzi...au naturel."

    menu:
        "Join Claudia in the jacuzzi":
            $claudia += 5
            $lust += 5
            #show screen lust5
            mc "Alright, Claudia. Let’s do this."

            scene d3jacuzzi030 with dissolve
            c "Mmm, that’s the spirit, darling."
            mc "This is… wild, Claudia. You don’t hold back, do you?"
            c "Why should I? I like living free, [player_name]. And I think you do too."

            scene d3jacuzzi090 with dissolve
            c "Come, let the water melt your worries away."

            scene d3jacuzzi126 with dissolve
            c "Mmm, look at you, all bold and bare. The water feels good, doesn’t it?"
            mc "Yeah, Claudia, this is… wild."

            #scene d3jacuzzi115 with dissolve
            #c "Intense is how I live, [player_name]. No point in half-measures."
            # Claudia shifts, her body gliding closer through the steam, her breasts rising slightly above the water, glistening like polished marble. Her smile is a challenge, daring him to match her boldness.

            scene d3jacuzzi127 with dissolve
            c "You’re showing off a little, but I want to see more of you, darling. All of you. Don’t be shy now—let me see what you’re really working with."
            mc "You’re not subtle, are you, Claudia?"
            jump claudia_sex

        "Go back to Rachel":
            mc "I… I should head back to Rachel. This is too much for me right now."


            scene d3jacuzzi150_ng with dissolve
            c "Suit yourself, darling. But you know where to find me."
            mc "I’ll catch your show tomorrow, Claudia. I need to get back to Rachel."
            jump game_night



    return

label claudia_sex:
    menu:
        "Show more to Claudia":
            mc "Alright, you asked for it."
            $claudia += 10
            $lust += 10
            #show screen lust10

            scene d3jacuzzi141 with dissolve
            c "Oh, darling, now that’s what I’m talking about!"
            mc "Happy now? You’ve got quite the way of pushing things."

            scene d3jacuzzi137 with dissolve
            c "Very happy, [player_name]. You’re full of surprises, aren’t you? Let’s see how much more fun we can have."
            jump claudia_sex2

        "Decline politely":
            mc "I think I’m good like this, Claudia. Let’s keep it… relaxed."
            scene d3jacuzzi130 with dissolve
            c "Playing it safe, huh? That’s alright, darling...I’ve got time to wear you down."
            mc "Maybe next time, Claudia. This is plenty for now."

            #scene d3jacuzzi120 with dissolve
            scene d3jacuzzi100 with dissolve
            c "Oh, there’ll be a next time, [player_name]. I always get what I want."
            mc "Bye Claudia"

            scene d3jacuzzi150_ng with dissolve
            c "Bye for now [player_name]...See you tomorrow at the Show Bar."
            jump game_night

    return





label claudia_sex2:

    mc "Claudia, you’ve got a way of making everything feel electric."

    scene d3jacuzzi129 with dissolve
    c "Electric’s just the start, darling. But this jacuzzi’s getting a bit… confining. How about we take this to the patio? I’ve got a cozy sofa out there, perfect for getting… closer."
    mc "The patio? You don’t slow down, do you?"

    scene d3claus020 with dissolve
    c "Here we are, darling. Sit down, make yourself comfortable."
    mc "Comfortable’s one way to put it."

    scene d3claus040 with dissolve
    c "Let’s see how much more comfortable we can get."
    mc "Fuck, Claudia… that’s… incredible."

    ### Play video 2 loops
    $ renpy.movie_cutscene("/images/claudia.webm", loops=2, delay=None)

    scene d3claus056 with dissolve
    c "Mmm, you taste as good as you look, [player_name]. But I want more. Ready for me?"
    mc "God, Claudia, you’re something else."

    scene d3clauride020 with dissolve
    c "Oh, darling, you fill me so good."
    mc "You’re… fucking amazing, Claudia."

    scene d3clauride030 with dissolve
    c "Keep going, [player_name]… I want it all!"

    scene d3clauride060 with dissolve
    c "Ohh, [player_name], you’re driving me wild!"
    mc "Claudia… shit, you’re too much!"

    #scene d3claus050 with dissolve
    scene d3claus060 with dissolve
    c "Not yet… I want something special."

    scene d3claus030 with dissolve
    c "Finish on me, [player_name]. I want your cum on my face, my tits… let me see it, taste it."

    scene d3claus031 with dissolve
    mc "Fuck, Claudia… you’re unreal."

    scene d3claus032 with dissolve
    c "Mmm, come on, darling!"

    scene d3claus033 with dissolve
    c "Yes, [player_name], give it to me… now!"

    scene d3claus034 with dissolve
    c "Mmm, so good… let me clean you."
    mc "Goddamn, Claudia… that was… insane."

    scene d3claus036 with dissolve
    c "Mmm, you didn’t disappoint. You’d better be at the Show Bar tomorrow night. I want you watching… thinking about this."
    mc "I’ll be there, Claudia. No way I’m missing that."

    scene d3claus035 with dissolve
    c "Good. Now get back to Rachel. But don’t forget me."
    mc "Yeah, I should go. See you tomorrow, Claudia."

    jump game_night
    return





#### game night
label game_night:
    scene d3game040 with dissolve
    mc "Hi there, I'm back"

    scene d3game030 with dissolve
    r "Oh, [player_name], good you’re here. I owe you an apology. I got upset earlier about those beach photos, but Lucy explained it was just harmless fun."
    l "Told ya, Mom, it was no biggie! Just me goofin’ off for the camera."

    scene d3game040 with dissolve
    mc "Glad it’s sorted. That game looks intense. Rachel, you holding up okay?"

    scene d3game050 with dissolve
    r "I’m doing just fine, thank you. I’ve got this in the bag."
    mc "If you say so, Rachel, I’ll stick around and watch you play, if you don’t mind."

    scene d3game060 with dissolve
    l "Pfft, Mom, you’re down to, like, a few chips! I’m totally gonna wipe the floor with you."
    mc "Lucy’s got a point, Rachel."

    scene d3game070 with dissolve
    r "Oh, hush, both of you. I’ve come back from worse. One good hand, and I’ll have Lucy begging for mercy."

    scene d3game080 with dissolve
    l "Bet you won’t, Mom! Let’s make this fun. If I win, I get to pick your bikini for the beach tomorrow. Deal?"

    scene d3game096 with dissolve
    r "A bikini? Lucy, you’re incorrigible. Fine, deal. But you’d better start planning your defeat instead."


    scene d3game091 with dissolve
    l "Oh my gosh, Mom, you’re toast! One more hand, and I’m picking out the teeniest bikini for you! It’s gonna be, like, totally iconic. You’ll be the hottest mom on the beach!"


    scene d3game095 with dissolve
    r "I’m not done yet. One good hand, and I’ll turn this around."

    scene d3game120 with dissolve
    l "Dream on, Mom! This is it—check this out!"
    r "Oh, Lucy… I can’t believe I lost."
    scene d3game100 with dissolve
    l "Yesss! I win, I win! Oh, Mom, this is gonna be so epic! I’m picking the perfect bikini—something to make jaws drop!"
    scene d3game110 with dissolve
    r "Please, sweetheart, don’t pick something too… too revealing."
    mc "Well, Rachel, looks like Lucy’s got the upper hand. A bet’s a bet, you know."

    scene d3game120 with dissolve
    r "I know, I know… but, Lucy, please, nothing too outrageous. I’m begging you."

    scene d3game136 with dissolve
    l "No promises, Mom! You’re gonna look so hot, you’ll thank me later. Right, [player_name]?"
    mc "A deal’s a deal, Rachel. Let’s see what Lucy comes up with. Could be fun."

    scene d3game138 with dissolve
    l "Oh, [player_name], you’re gonna {b}love{/b} the bikini I’m picking for Mom tomorrow. It’s gonna be so hot, you won’t know where to look!"

    scene black06 with dissolve
    centered "End of Day 3"
    #centered "Please save here"

    jump day4

    return

################### DAY 2 #################################

label tothebeach:
    play music musica5 loop
    scene black01 with dissolve
    scene black02 with dissolve
    centered "\n\nThe second day in the morning, you all decide to go to the beach together."
    scene goingtothebeach033 with dissolve
    r "Are you sure this isn’t too crowded? I just… I feel a bit exposed in this new swimsuit. "
    mc "Relax, Rachel. It’s just a handful of people. Besides, you look incredible. No reason to hide."
    scene goingtothebeach010 with dissolve
    r "I’m not exactly a bikini model, you know? Not like some people who can just… flaunt everything."
    l "Ugh, Mom, you’re acting like you’re wearing a potato sack. Wait till you see my swimsuit: it’s literally fire."
    scene goingtothebeach030 with dissolve
    l "And [player_name], you’re gonna love this bikini: it’s, like, next-level. You’ll see, I’m basically the main event today."
    mc "Main event or not, Lucy, let’s keep the chaos to a minimum, yeah? Rachel, you’ve got nothing to worry about."
    scene goingtothebeach034 with dissolve
    r "I still think we should’ve stayed at the apartment. This sun is brutal, and... well, I don’t know if I’m beach-ready."
    mc "Rachel, you look great. Besides, it’s just us and the crabs out here."
    scene goingtothebeach039 with dissolve
    r "Okay... okay, fine. You win. Let's go."
    #scene goingtothebeach030 with dissolve

    scene goingtothebeach050 with dissolve
    r "Oh, this spot looks perfect! Not too crowded, and we'll get plenty of sun."
    l "Finally! Time to really soak up some rays... and show off my new bikini!"
    scene goingtothebeach070 with dissolve
    l "Ta-da! Isn’t this fire? I got it online. It’s called ‘Barely There Chic’!"
    r "Lucy! That’s... that’s not a bikini, that’s dental floss!"
    mc "Uh, it’s... bold. Very, uh, modern."
    scene goingtothebeach075 with dissolve
    l "See? [player_name] gets it. Wait ‘til you see the bottom!"
    r "Lucy! cover yourself! What if someone sees?"
    scene goingtothebeach090 with dissolve
    l "Mom, it’s literally just us. And [player_name]’s not complaining, right?"
    mc "I’m... staying neutral."
    r "Well, I suppose... it is a beach. Just try not to get too much sun."
    scene goingtothebeach100 with dissolve
    l "That's the point, Mom! It's supposed to be barely there. It's totally in style, and it's perfect for getting an all-over tan!"
    r "Honestly, Lucy, I just don't understand these things. But fine, fine, do what you like."
    mc "Alright, girls, let's calm down. The sun's waiting, and so is this perfect spot. How about we just get these towels laid out and start soaking up some rays?"
    scene beach010 with dissolve
    r "You were right, darling. It really isn't busy at all. Just a few families further down. I feel... much more comfortable."
    mc "See? Told you. And this spot is perfect, really."

    scene beach040 with dissolve
    r "Right then, sun cream time. Don't want to get burnt on our first day."
    scene beach050 with dissolve
    l "Ugh, fine. Mom, don't miss a spot!"

    scene beach050_2 with dissolve
    r "Oh, [player_name], darling? My back is always so hard to reach properly. Would you mind terribly?"
    scene beach050_3 with dissolve
    l "Me too, [player_name]! My shoulders get totally fried if I don't get them. And you know how sensitive my skin is!"

    menu:
        "Who do you apply sunscreen to first?"
        "Rachel":
            jump sunscreen_rachel
        "Lucy":
            jump sunscreen_lucy

    return

label sunscreen_rachel:
    scene beach100 with dissolve
    mc "Alright, Rachel, let’s keep you from turning into a tomato."
    r "Thanks, [player_name]. Just... don’t miss any spots. I burn easily."
    ### MIRAR dits creuen cellphone
    scene beach085 with dissolve
    l "Ugh, Mom, you’re hogging him! Hurry up, I’m next."
    scene beach105 with dissolve
    r "Patience, Lucy. This isn’t a race."
    mc "Rachel, darling, just close your eyes. Really relax into it. Think of nothing but the sun on your skin, and my hands making sure you don't burn."
    r "Okay, okay, bossy. Anything for a good tan."

    scene beach086 with dissolve
    l "Oops, silly thing keeps moving. Oh well!"
    mc "Uh, Lucy, your... uh, bikini’s staging a jailbreak."
    scene beach096 with dissolve
    l "What? Oh, no biggie. It’s just us, right?"
    scene beach125_2 with dissolve
    r "Thanks, [player_name]. That feels... nice."
    jump after_sunscreen

    return

label sunscreen_lucy:
    scene beach070 with dissolve
    mc "Alright, Lucy, let’s keep you from frying."
    l "Yesss, my hero! Make sure you get everywhere, okay?"
    scene beach080 with dissolve
    l "Mmm, you’re good at this, [player_name]. Ever think about going pro?"
    mc "Pro sunscreen applicator? I’ll stick to my day job, thanks."
    scene beachdtits with dissolve
    scene beachdtits3 with dissolve
    l "Whoopsie! This thing’s so slippery. You saw nothing, right?"
    scene beachdtits2 with dissolve
    mc "Saw nothing? I’m practically blind now."
    scene beachdtits2 with dissolve
    l "Thanks, [player_name]. You’re the best."
    jump after_sunscreen

    return


label after_sunscreen:
    scene beach_discuss020 with dissolve
    r "Lucy, I still can’t believe you wore that... that napkin to the beach. What happened to the cute one-piece I bought you?"
    l "Mom, that thing was for, like, grandmas. I’m eighteen, I wanna look hot!"
    scene beach_discuss030 with dissolve
    r "Hot? You’re going to give [player_name] the wrong idea!"
    scene beach_discuss010 with dissolve
    l "Maybe I want to give him ideas. Right, [player_name]?"
    mc "Ladies, don’t drag me into this."
    r "Oh, please, Lucy. He’s with me. Stop acting like you’re in a music video."
    scene beach_discuss040 with dissolve
    l "Whatever, Mom. At least I’m not paranoid about every seagull checking me out."
    mc "Okay, you two, I’m gonna take a walk before I start refereeing. Try not to start a sand war while I’m gone."
    #scene beach_discuss050 with dissolve
    scene beach155 with dissolve

    r "Fine, go. Maybe Lucy will calm down by the time you’re back."
    l "Me? You’re the one freaking out over nothing!"
    mc "Bye!"

    return


label mabel:
    scene beach197 with dissolve
    mc "{i}Another quiet day by the sea...{/i}"
    mc  "{i}Hmm? What's that?{/i}"
    scene beach198 with dissolve
    scene beach199 with dissolve
    scene beach200 with dissolve

    u "Oh no! My ball! It's getting away!"

    scene beach210 with dissolve
    mc "Got it!"
    scene beach220 with dissolve
    sar "Oh, thank you so much! You're a lifesaver. I'm Sara, by the way."
    mc "Here you go. [player_name]. Nice to meet you, Sara."
    scene beach230 with dissolve
    sar "It's really nice to meet you too, [player_name]. I'm usually not so clumsy."
    scene beach240 with dissolve
    u "Sara! There you are, you little runaway!"
    sar "Hi Mom"
    scene beach250 with dissolve
    w "Hey there, photographer! Fancy seeing you again."
    scene beach281 with dissolve
    u "And who’s this handsome stranger?"
    scene beach280 with dissolve
    sar "Mom, this is [player_name]. He saved my ball. Don’t make it weird."
    mab "Weird? Me? I’m Mabel. Nice to meet you, [player_name]."
    #scene beach270 with dissolve

    #Transition: from top to bottom in 4 seconds
    scene mabel_vertical2 with dissolve:
        xalign 0.0 yalign 1.0 zoom 1
        linear 8.0 yalign 0.0
    pause 8.0
    pause 2.0
    mc "Uh, likewise, Mabel. That’s quite the... outfit."
    mab "This old thing? It’s just here to make the seagulls jealous."
    scene alinabeachhello2 with dissolve
    w "Good morning [player_name]"
    mc "Good to see you again Alina"
    scene beach282 with dissolve
    sar "Wait, you know him, Alina?"
    #scene beach270 with dissolve
    w "Oh, Sara, don’t get jealous already. [player_name] and I had a little... photo session yesterday. Right, [player_name]? I see you’ve met Mabel and Sara."
    scene alinabeaachhello with dissolve
    mc "Yeah, just met Sara and Mabel."
    scene beach260 with dissolve
    mab "Hold up. You’re the guy who took Alina’s special photos yesterday? I’m feeling left out, and that’s not my style."
    mc "Ah, well, Alina and I... we collaborated on a few artistic shots, yes. She was a wonderful subject."
    scene beach281 with dissolve
    mab "My phone's practically a dinosaur. Would you mind lending your artistic eye, and your device, to a lady in need of some new profile pictures?"
    mc "My device is at your service, Mabel. What did you have in mind?"
    scene beach280 with dissolve
    sar "Mom, seriously? You’re doing this {b}now{/b}? I’m out."

    scene beach283 with dissolve
    mab "Don't worry, [player_name]. Sara will come back soon."
    scene photobeach010 with dissolve
    mab "Alright, [player_name], let’s make magic. Snap away!"
    mc "Okay, uh, maybe pose like you’re... owning the beach?"

    scene photobeach020 with dissolve
    mab "Owning? Sweetie, I’m the queen of this coast."

    scene photobeach066 with dissolve
    #### USAR 62 64 o 66
    mab "What do you think, [player_name]? Time to set this thing free?"
    mc "Free? It’s already staging a breakout."

    scene photobeach072 with dissolve
    #### USAR 72
    mab "There. Art in motion. Keep shooting, maestro."

    scene alina_cheers2 with dissolve
    w "Mabel, you’re a goddess! "

    scene mabel_invites_alina with dissolve
    mab "Alina, darling, don't just stand there! Join the fun! "
    w "Okay, you know what? You're right!"

    scene mabel_invites_alina20 with dissolve
    w "It's a beautiful day, and why not? If you're going to be gorgeous and free, so am I!"
    mab "There you go!"

    scene mabel_invites_alina40 with dissolve
    w "Whew! That feels good already!"
    mab  "Oh, my beautiful Alina! Look at you, absolutely radiant!"

    scene mabel_invites_alina50 with dissolve
    mab "Ok, let’s make it a duo shoot. Ready for double trouble?"
    w "A 'duo shoot,' you say? Sounds like a wonderfully scandalous idea."
    mc "Alright, ladies, how about something... collaborative? Back to back, facing me. Let's see that synergy!"

    scene photobeach105 with dissolve
    mab "Ooh, I like the sound of 'synergy'! Alina, you heard the man. Let's give him a show he won't forget."
    w "Sounds fun!"
    mc "Perfect! Hold that! The light is incredible on you two."

    scene photobeach145 with dissolve
    w "Feeling pretty incredible, actually! This is fun, Mabel!"
    mab "Told you, darling! Nothing like a little exhibitionism to get the blood flowing. Now, [player_name], are you getting our best sides?"

    scene alina_mable_beach_080 with dissolve
    mc "Every side is your best side, Mabel. But let's try something else. Turn around, both of you. Let's see those... assets from a different angle."

    scene photobeach115 with dissolve
    w "Is this what you had in mind, photographer?"

    scene photobeach135 with dissolve
    mab "Oh, I think I know {b}exactly{/b} what he has in mind. And I aim to please!"
    mc "Wow. Mabel, you're... truly committed to the art."

    scene photobeach125 with dissolve
    mc "Alright, let’s switch it up. Mabel, how about you turn around just a bit?"

    scene photobeach115 with dissolve
    mab "Oh, I love it! Back to the camera, like we’re teasing the world!"
    w "This is epic! [player_name], you’re gonna need a new phone after this."

    scene alina_mable_beach_050 with dissolve
    #scene alina_mabel_beach051 with dissolve
    mab "Alright, [player_name], we're giving you our all. Now, how about you join us?"
    w "Yes, come on, [player_name]! It's only fair, isn't it? Get rid of those trunks and truly experience the moment with us."
    mc "Me? Uh...I don't know... I'm supposed to be behind the camera."

    scene alina_mabel_beach041 with dissolve
    mab "Oh, imagine the connection. It'll be so much more... authentic."
    w "Exactly. Don't be shy with us."
    mc "Okay... okay, you've convinced me."

    scene alina_beach_020 with dissolve
    mc "Now, how about you two try posing sitting on the sand? It might give us a different feel."
    mab "Sitting on the sand? Ooh, I like it! Very earthy, very natural."

    scene alinamabel021 with dissolve
    w "Perfect! We can work with that. Though, [player_name], I think you're already feeling the 'natural' part quite intensely, aren't you?"
    mab "He does seem a little... excited about the idea, doesn't he, Alina? Don't worry, [player_name], it's just us. No need to hide anything."


    scene sararrivesbeach010 with dissolve
    sar "Mom? [player_name]? What is this, a nudist colony audition?"
    scene photobeach330 with dissolve
    mab "Sara, it’s just beach photography! Wanna join? [player_name]’s got the magic touch."
    sar "Join? I’d rather wrestle a jellyfish. This is so embarrassing."
    scene photobeach320 with dissolve
    w "Oh, Sara, it’s fun! You should see the pics we’re getting."
    mc "Yeah, it’s... uh, creative. No pressure, Sara."

    menu:
        "What do you do about Sara?"
        "Try to convince Sara to join the shoot":
            jump convince_sara
        "Let Sara leave, keeping the focus on Mabel and Alina":
            jump let_sara_leave

    return


label convince_sara:
    mc "Hey, Sara, it’s just us having a laugh. You could totally join in, make it a family thing."
    mab "Yeah, sweetie, you’re gorgeous! Let’s make some memories, bikini or not."

    scene photobeach310 with dissolve
    sar "You guys are nuts. I... fine, I’ll stay. But don’t expect me to go full crazy like you."
    mc "Sara, you’re already rocking that bikini. Just strike a pose, whatever feels right."
    sar "Okay, but if these pics end up online, I’m moving to Antarctica."
    scene photobeach350 with dissolve
    mab "That’s my girl! You’re a star, Sara!"
    sar "Oh... I don't know. I'm so... small. And Mom has such... big boobies..."
    mc "Sara, it's not about size. It's about confidence. And you have a beautiful smile, and a wonderful spirit. That's what truly shines."
    sar "Really? You... you think so, [player_name]?"
    scene photobeach360 with dissolve
    mab "Sara, darling, let's show him what real family bonding looks like!"
    sar "Mom! Can't breathe! And... and your... your boobs are everywhere!"
    mab "Nonsense, darling! More to love! Now, let's get a shot of us, mother and daughter"

    scene photobeach395 with dissolve
    sar "Oh, no, Mom! Not like this! My face is going to be squished! And your... they're so... big!"
    w "Alright, girls! I'll be the audience for this part. You two are amazing!"

    scene photobeach385 with dissolve
    mc "Hold that pose, ladies! Sara, try to relax into it! It's all about the natural expression!"
    sar "Relax? With Mom's... boobs... right here? I'm trying, [player_name], I really am!"

    scene photobeach375 with dissolve
    mab "She'll get used to it! It's good for her to see what a real woman looks like, eh, [player_name]?"
    mc "Alright, ladies, let’s capture some magic! Sun’s blazing, waves are dancing, and my camera’s ready for this... unique shoot."

    scene photobeach370 with dissolve
    mab "Unique? Sweetie, this is freedom in high definition! The breeze on my skin is basically poetry."
    sar "Mom, can you not? I’m already feeling like the odd one out in my bikini."

    scene photobeach405 with dissolve
    mc "You both look amazing, Sara. Really. Just be yourselves"
    sar "I’m just trying not to die of embarrassment here, [player_name]."

    scene photobeach374 with dissolve
    sar "This is too much. I... I can't do this. I'm sorry. I just... I need to go."

    scene sarashyleave032 with dissolve
    mab "Oh, Sara, my poor girl...It was too much for her, wasn't it? Me, like this... and her, still so unsure of herself."
    mc "You're right, Mabel. It's a tough age. Maybe we should head back and just check out the photos we did get."


    jump ending_show

    return


label let_sara_leave:
    scene sarashyleave010 with dissolve
    mc "Sara, no stress. If this isn’t your scene, go enjoy your ball."
    sar "Thanks, [player_name]. I’m... gonna go build a sandcastle or something normal."
    scene sarashyleave032 with dissolve
    mab "Oh, my poor girl. She saw us in our birthday suits and bolted like a scared seagull. Too much for her."
    scene sarashyleave020 with dissolve
    w "Shame. She’s cute when she’s flustered. Bet she’s hiding behind a dune, cursing our confidence."
    mab "She’s just shy. And maybe a tad jealous. Not everyone can rock this like we do."


    scene alina_mabel_beach041 with dissolve
    mab "Never mind her, [player_name]. Alina and I still have so many angles to explore, so many moments for you to capture."
    w "Yes, [player_name]. We want you to capture all of it."
    scene mabel_alina_final_010 with dissolve
    mc "Yes! Just like that. You are absolutely breathtaking."
    w "Oh, [player_name]... I've never felt so... free. So seen."
    mc "I want you both to turn to face each other. Close, intimate."
    scene photobeach100 with dissolve
    mc "Perfect. Stay right there. Just look at each other. Let the sea be your witness."
    mc "You both did more than well. You were incredible. Every single shot is a treasure. Come here, take a look. I think you'll be... very pleased with yourselves."

    jump ending_show

    return

label ending_show:

    scene ap30 with dissolve
    w "You really have an eye, [player_name]. These are going to be amazing."

    scene afterphotos11 with dissolve
    mab "So, [player_name], what's the plan now? More photos? Or perhaps something a little more... private? This beach is full of secluded spots, if you know where to look."
    w "I'm also open to suggestions, [player_name]."

    mc "{i}This is it. The moment of truth. Do I play it safe, or dive headfirst into temptation? Rachel and Lucy are probably still sunbathing... but these two...{/i}"



    menu:
        "Suggest going with Alina alone.":
            scene alina_choosen with dissolve
            mc "Alina, I'd love to explore some of those secluded spots with you. Just the two of us."
            w "Really? I'd like that very much, [player_name]. Mabel, I'll catch you later. We have some... artistic discussions to continue."
            mab "Oh, I understand perfectly. Go on, you two. Don't let an old gal like me hold you back."


            jump ending_alina_alone

        "Suggest going with Mabel alone.":
            scene mabel_choosen with dissolve
            mc "Mabel, I think I'd prefer to see those secluded spots with you. Just us."
            mab "Oh, you charmer! I knew you had good taste. Alina, darling, I'll see you later. [player_name] and I have some... private matters to discuss."
            w "Alright, Mabel. Have fun, you two."

            jump ending_mabel_alone

        "Try to go with both women together.":
            scene none01 with dissolve
            mc "You know, I think a trio would be even more fun. What do you say, ladies? All three of us, exploring the beach?"
            mab "A trio, you say? Now, [player_name], I'm not sure I'm the sharing type when it comes to... certain pleasures."
            w "Yeah, [player_name]. I'm looking for something a bit more... focused. I like my attention undivided, if you know what I mean."
            scene none02 with dissolve
            mab "Indeed. Some things are best enjoyed one-on-one. Don't be greedy, handsome. Choose wisely."
            mc "Ah. Right. Understood."

            jump sara

        "Decide to go back to Rachel and Lucy.":

            mc "You know what, ladies? This has been... incredibly enlightening. But I should probably head back. Rachel and Lucy will be wondering where I've gotten to."
            scene alina_mable_beach_050 with dissolve
            scene none02 with dissolve
            mab "Oh, what a shame. Just when things were getting interesting. Duty calls, I suppose."
            w "Too bad, [player_name]. Thank you for these... incredible memories."

    return


label ending_mabel_alone:
    scene mabel_sx01 with dissolve
    mab "Here. No prying eyes. Just us. And your... curiosity."
    mc "Privacy is always appreciated, Mabel. Especially for moments like this."

    $mabel += 10
    $lust += 10
    #show screen lust10

    scene mabel_sx02 with dissolve
    mab "You have quite the... instrument, don't you, [player_name]?"
    mc "It certainly has its moments. Especially when it's admiring such a beautiful view."

    $mabel += 10
    scene mabel_sx03 with dissolve
    mab "So sensitive, just how I like it. Responsive. Eager."
    mc "You've got a touch, Mabel. A very persuasive touch."


    scene mabel_sx04 with dissolve
    mc "Oh, yes... You definitely know how to make a man feel... appreciated."

    scene mabel_sx05 with dissolve
    mc "You're playing a dangerous game, Mabel. And I'm more than willing to play along."
    mab "Oh, don't worry, darling. This is just the warm-up. The main event is yet to come."

    scene mabel_sx12 with dissolve
    mab "Now. It's time for me to take the lead. Unless you prefer to be in charge, [player_name]?"
    mc "Lead the way, Mabel. I'm all yours."

    scene mabel_sx06 with dissolve
    mab "Ahhh... yes. That's it. Perfect. So full."
    mc "God, Mabel... you feel incredible. So warm... so tight."

    scene mabel_sx07 with dissolve
    mab "Oh, God, [player_name]... yes... fuck me... baby... harder...!"
    mc "That's it, Mabel! Ride me! Just like that! You're amazing!"

    scene mabel_sx11 with dissolve
    mab "I'm coming... oh, God... I'm coming! Faster, [player_name]! Push it in me! All of it!"
    mc "Give it to me, Mabel! Let it all go! I'm right here with you!"

    scene mabel_sx08 with dissolve
    mab "Oh, [player_name]... that was... incredible."
    mc "Absolutely, Mabel. Truly unforgettable. But I really should get back to Rachel and Lucy before they wonder where I've gone."
    mab "Of course, darling. Don't keep them waiting too long."


    jump sara

    return


label ending_alina_alone:

    scene alina_sx01 with dissolve
    w "You... you really chose me, [player_name]?"
    mc "Absolutely, Alina. You captivate me."

    $alina += 10
    $lust += 10
    #show screen lust10

    scene alina_sx05 with dissolve
    w "Is this what you want, [player_name]? My mouth. For you?"
    mc "More than anything, Alina. Show me."

    $alina +=10
    scene alina_sx02 with dissolve
    scene alina_sx03 with dissolve
    scene alina_sx02 with dissolve
    scene alina_sx03 with dissolve
    scene alina_sx02 with dissolve

    w "Mmm... so big... so good, [player_name]."
    mc "Alina... oh, God... you're incredible."

    scene alina_sx07 with dissolve
    w "Now... let's try something else. I want to feel you... all of you. From behind."
    scene alina_sx06 with dissolve
    w "Come here, [player_name]. Take me. Hard."
    mc "Oh, I will, Alina. I absolutely will."
    scene alina_sx08 with dissolve
    mc "You're so beautiful, Alina. Every inch of you."
    w "Ahhh... yes... oh, [player_name]! That's it! Deeper!"
    scene alina_sx12 with dissolve
    mc "You feel amazing, Alina... so tight... so wet."
    w "Faster, [player_name]! Please! I'm so close... so close!"
    scene alina_sx13 with dissolve
    w "Ahhhhh"

    scene alina_sx09 with dissolve
    w "Well, now. That was certainly... everything I hoped for, darling."
    mc "And more, Alina. Much more. . But I really should get back to Rachel and Lucy now. They'll be wondering where I've gone."
    w "Of course, darling. Duty calls. But do stop by again, won't you? There's always more to explore."

    jump sara

    return


label sara:
    scene seaside with dissolve
    mc "{i}Time to head back and see what Rachel and Lucy were up to.{/i}"
    scene sara010 with dissolve
    mc "{i} There’s Sara again. She didn’t notice me yet. Should I say hi, or just keep walking back to Rachel and Lucy?{/i}"

    # Player choice
    menu:
        "Greet Sara":
            jump sara_conversation
        "Keep walking to Rachel and Lucy":
            jump return_to_girlfriend
    return

label sara_conversation:
    mc "Sara? Hey there."
    scene sara020 with dissolve
    sar "Oh! [player_name]! Hi. I, uh... I thought you were still with them."
    mc "Just finished up. You seemed to leave in a hurry earlier. Everything alright?"
    scene sara030 with dissolve
    sar "It's just... I saw. You know. Mom and Alina."
    mc "Ah."
    scene sara040 with dissolve
    sar "Do you... do you like me?"
    scene sara050 with dissolve
    sar "I know I'm... I'm flat. Not like Mom. Or even Alina. Is that... is that why you like them more?"
    mc "Sara, no. That's not it at all. You're beautiful. You're pretty exactly the way you are. Believe me."
    scene sara030 with dissolve
    sar "But how can I know? I mean, really know? You just said that because... well, because you're nice."
    scene sara060 with dissolve
    sar "Don’t laugh, okay? I’m gonna… do something brave. Like Mom-level brave."
    scene sara070 with dissolve
    mc "Well, damn, Sara! That’s a bold opener."
    sar "Stop it! I’m not done yet."
    scene sara080 with dissolve
    sar "Okay, um… how’s this? Am I… exciting yet?"
    mc "Sara, you’re like a firecracker in a sparkler factory. My heart’s doing backflips."
    scene sara090 with dissolve
    sar "You’re just saying that. I’m not… you know, like Mom."
    scene sara100 with dissolve
    sar "There! Now tell me the truth. Am I… doing anything for you?"
    mc "Sara, you’re a walking sunset—stunning and impossible to look away from. Trust me, you’re doing plenty."
    scene sara110 with dissolve
    sar "Really? Like… really really? I need proof. Actual proof."
    mc "Proof? What, you want me to draw a diagram? ‘Anatomy of a Beach Crush’?"
    scene sara120 with dissolve
    sar "No! I mean… show me. If I’m exciting, then… you’d be, you know, excited. Right?"
    mc "You’re turning this into a science fair project, Sara. Okay, fine, but if a seagull files a complaint, you’re taking the blame."
    scene sara116 with dissolve
    mc "There. You happy? You’ve got me more worked up than a kid at a candy store."
    sar "Oh… wow. Okay. That’s… definitely proof."
    $sara += 5
    $lust += 10
    #show screen lust10
    scene sara140 with dissolve
    sar "I didn’t think you’d… okay, um, now I feel like I need to… do something back."
    mc "Sara, you’ve already gone full superhero with the bravery thing. You don’t need to do more."
    scene sara150 with dissolve
    sar "No, I want to. I’ve never… done anything like this. But I want to try. For you."
    mc "Whoa, Sara, you sure? "
    scene sara_bj05 with dissolve
    $sara += 10
    sar "Shush! I’m… figuring it out. I’m a quick learner, okay?"
    mc "Okay, Sara, you’re… uh, definitely earning a gold star for effort."
    scene sara_bj12 with dissolve
    sar "Stop talking! You’re making it worse!"
    scene sara_bj12_2 with dissolve
    sar "I’m trying to be sexy! Don’t ruin my moment!"
    scene sara_bj05 with dissolve
    mc "I'm close, Sara... so close... I can't hold back..."
    stop sound fadeout 2.5
    scene sara_bj13 with dissolve

    scene sara_bj13_2 with dissolve
    mc "AAAHHH!"
    scene sara_bj17 with dissolve
    scene sara_bj19_2 with dissolve
    scene sara_bj20 with dissolve
    scene sara_bj22 with dissolve
    sar "Oh God, was that… okay? I know it was probably terrible."
    mc "Terrible? Sara, you were fantastic. A-plus for guts and charm."
    sar "Really? You’re not just sparing my feelings?"
    scene sara_bj24 with dissolve
    mc "Cross my heart. You’ve got serious potential."
    sar "Hah, okay. I’ll take it. But… don’t tell anyone. Especially not Mom."
    scene sara_bj26 with dissolve
    mc "My lips are sealed. "
    sar "Wow, that was... um, really intense, wasn’t it?You...you were flooding...."
    mc "Yeah, Sara, that’s putting it mildly."
    scene sara_leave with dissolve
    sar "Good. I’m… gonna go jump in the water. Cool off. Maybe hide from the world."

    jump return_to_girlfriend

    return

label return_to_girlfriend:
    scene seaside with dissolve
    mc "{i}Now let's see what Rachel and Lucy were up to.{/i}"

    scene beach155 with dissolve
    r "There you are, [player_name]! We were about to send out a search party. Where’d you wander off to?"
    mc "Nah, just… soaking in the scenery. You know, waves and stuff."
    scene beach040_2 with dissolve
    l "Ugh, you’re so weird. Mom, can we get ice cream already?"
    mc "yeah, let's go for an ice cream now"

    jump ice_cream

    return


label ice_cream:
    scene black01 with dissolve
    centered "\n\nYou decide to go enjoy some ice cream together."

    scene icecreamshop_enter010 with dissolve
    mc "Alright, an ice cream break. Perfect way to cool down after the beach."
    r "I hope they have something nice. I'm craving a really good sundae."
    l "Ugh, my bikini is still all wet. It's sticking to me. So annoying."
    scene icecreamshop02 with dissolve
    cryst "Welcome, welcome! Come right in! Find yourselves a cozy spot. I'm Crystal, and I'll be your sweet guide today."
    mc "Thank you, Crystal. This looks like a lovely spot."
    scene icecreamshop020_3 with dissolve
    r "It's very charming. A bit old-fashioned, but charming."
    l "Ugh, I seriously need to get this wet bikini off. It's chafing."
    r "You should have done that before we came in, Lucy."
    scene icecreamshop040 with dissolve
    l "I'll be right back. Don't order anything without me!"
    r "Honestly, that girl. No patience."


    scene icecreamshop310 with dissolve
    l "Ah, much better! So much lighter without that wet thing sticking to me. What do you think, [player_name]? Does this look better?"
    r "Lucy! Honestly! Must you do that here? In the middle of an ice cream shop?"
    l "What? I'm just getting comfortable! Feels good to stretch out after being cooped up in that wet thing."


    scene icecream170 with dissolve
    cryst "Alright, team! Ready for some more deliciousness? For something refreshing, our strawberry slushie is absolutely divine. Perfect for a warm day like this."
    scene icecream180 with dissolve
    r "Ooh, a strawberry slushie sounds perfect!"
    l "Make that two! Sounds amazing, Crystal."

    scene icecream170 with dissolve
    mc "I'm still not sure..."
    scene icecreamshop340 with dissolve
    cryst "Tell you what, why don't you come over to the counter? I can show you some of our specials up close."
    scene icecream240 with dissolve
    mc "Sure, why not? Lead the way"

    scene icecreamshop04 with dissolve
    mc "By the way, I don't think I properly introduced myself. I'm [player_name]."
    cryst "It's a pleasure to meet you, [player_name]. I'm Crystal, as you know. So, what are you in the mood for, handsome? Something sweet? Or perhaps... something a little more adventurous?"
    mc "Adventurous, you say?"
    scene icecreamshop05 with dissolve
    cryst "Absolutely. We have a dark chocolate chili that's just divine. Or maybe something else entirely catches your eye? Just between us, that one's always a big hit."
    mc "You know what, Crystal? Surprise me. I trust your judgment."

    scene icecreamtalk with dissolve
    l "Everything alright? You were gone a while."
    mc "Just so many delicious options! It was hard to choose."
    r "So, what did you get?"
    mc "It's a surprise."
    scene icecreamshop320 with dissolve
    cryst "Here you go, ladies! Two perfectly chilled strawberry slushies. And [player_name], your surprise is coming right up!"

    scene icecream190focus with dissolve
    mc "She isn't wearing any underwear. And Crystal is trans"

    scene icecream200 with dissolve


    menu:
        "(I'm not interested in her anymore.)":

            jump not_interested_crystal

        "(I'm even more interested in her now.)":

            jump more_interested_crystal

    return


label not_interested_crystal:
    scene icecreamshop330 with dissolve
    mc " Finally, I think I'll just stick to water today, Crystal. Thanks anyway."
    cryst " Oh... I understand. No problem at all, [player_name]."
    jump george_invite
    return


label more_interested_crystal:
    scene icecreamshop340 with dissolve
    mc " Actually, Crystal, I'm even more excited for that surprise now."
    cryst " Really? I'm glad to hear that, [player_name]. Very glad."
    mc "I'll just... I think I need to use the restroom first."
    scene icecreamshop350 with dissolve
    cryst "Of course. It's just through that door at the end."

    scene icecreamshop360 with dissolve
    mc "I'll be right back, ladies. Just a quick trip."
    r "Alright, don't be long."

    scene toilet010 with dissolve
    cryst "I think we need to talk, [player_name]. Just you and me. Don't you agree?"

    scene toilet020 with dissolve
    cryst "Just wanted to make sure you found everything alright. And... to offer a little something extra, if you're interested in a truly unique experience."
    cryst "I... I saw the way you looked at me. And I know what you're thinking. Most men... they don't understand. They see a woman, but they don't see me. And when they do... they often run."
    scene toilet030 with dissolve
    cryst "But I felt... something different from you. A kindness. An acceptance, maybe?"
    cryst "This is me. All of me. Do you... do you accept me? Do you find me desirable, even like this?"

    mc "{i}This is it. The moment of truth. She's putting everything on the line.{/i}"

    menu:
                "Accept Crystal":
                    scene toilet040 with dissolve
                    mc "Crystal... you're beautiful. And yes, I find you incredibly desirable. All of you."
                    cryst "Thank you, [player_name]. Thank you for seeing me. For truly seeing me."

                    scene toilet050 with dissolve
                    cryst "And you, [player_name], are looking rather... eager. Just as I like. Come here, darling. Let me help you with that."

                    scene toilet060_3 with dissolve
                    cryst "Oh, my. Such a beautiful thing. Just begging for attention, isn't it?"
                    mc "Crystal... you don't have to..."

                    scene toilet060 with dissolve
                    cryst "But I want to, [player_name]. Oh, I absolutely want to."
                    cryst "Mmm... so big... so delicious."

                    scene toilet100 with dissolve
                    cryst "Now, [player_name]. Let's make this really special."
                    scene toilet110 with dissolve
                    cryst "Ahhh... yes. So good. So full."
                    mc "Crystal! Oh, God, Crystal! You feel amazing! Don't stop!"
                    scene toilet130 with dissolve
                    cryst "I'm coming... Oh, [player_name]! I'm coming! Right now!"
                    scene toilet140 with dissolve
                    cryst "Ahhh! Yes! Oh, fuck! All of it! Right there!"
                    scene toilet160 with dissolve
                    cryst "Oh... wow... That was... perfect."
                    scene toilet170 with dissolve
                    mc "Perfect, Crystal. Absolutely perfect."
                    scene toilet180 with dissolve
                    mc "I should... I should get back. Rachel and Lucy will be wondering."
                    cryst "Go on, [player_name]. I understand. A man's duties, after all."

                    jump return_to_table_after_encounter

                "Politely reject Crystal.":
                    mc "Crystal, you're... truly beautiful. And incredibly brave. But I can't. I have my girlfriend and her daughter waiting."
                    scene toilet_sad with dissolve
                    cryst "I understand, [player_name]. Thank you for being so honest, and so polite about it."
                    scene toilet_maybe with dissolve
                    cryst "I just... I had to know. I'm always afraid of being rejected. But you were kind. It's rare to find such a gentleman. Perhaps... on another day, when the circumstances are different, our paths might cross in a more... opportune moment? I'll be here."
                    mc "Perhaps. Thank you, Crystal."

                    jump return_to_table_after_encounter


    return

label return_to_table_after_encounter:

    scene icecream250 with dissolve
    r "Finally! What took you so long?"
    mc "Just... a little busy in there. All good now."


    jump george_invite

    return


label george_invite:

    scene icecream300 with dissolve
    ge "Crystal, my dear! Looking as sweet as your sundaes today!"
    cryst "George! Good to see you! The usual, I presume?"
    ge "You know me too well, lass."

    scene icecreamgeorge010 with dissolve
    ge "Well, if it ain’t my favorite renters! [player_name], Rachel, Lucy. Fancy running into you here. I was just about to send you all a message, actually. Perfect timing!"
    mc "Hey, George! What's up?"

    scene icecreamgeorge020 with dissolve
    ge "Big news! Claudia's performing tonight at our show bar. A full set! It's going to be spectacular. I was hoping you'd all join me. My treat, of course!"
    r "Oh, a show bar? Hmm. I don't know, George. I was thinking of a quiet night in."

    scene icecreamgeorge030 with dissolve
    l "Rachel, come on! A show bar? It sounds like fun! We haven't been to one of those in ages!"
    mc "Yeah, Rachel. It'll be a good change of pace. And it's a chance to see a local performance. George seems really excited about it."
    r "But... it's a show bar. Won't it be loud? And... crowded?"

    scene icecreamgeorge040 with dissolve
    l "That's part of the charm! The excitement of something new! It'll be an adventure!"
    mc "Lucy's right. And who knows, it might be really interesting. It'll be an experience you won't want to miss."
    r "Hmm. Alright, alright! You two are relentless. Fine. But if it's too loud, I'm blaming both of you."

    scene icecreamgeorge050 with dissolve
    l "Yes! Knew you'd come around!"
    ge "Excellent! Knew I could count on you all! Fantastic! I'll reserve a table for you then. See you all tonight!"


    jump bar_scene

    return


label bar_scene:
    scene black02 with dissolve
    centered "After a relaxed dinner, you all decided to check out that Show Bar George mentioned earlier, the one connected to Claudia."

    scene basebarwelcome14 with dissolve
    mc "Here we are. George said he saved us a good spot."
    r "I hope so. I'm looking forward to a relaxed evening"
    l "This looks awesome!"

    scene basebarwelcome13 with dissolve
    ge "Ah, [player_name]! Rachel! And the young lady. Welcome, welcome! Your table is right at the front, perfectly positioned for the show tonight."
    mc "Thanks, George. Looks great."

    scene basebar_sara020 with dissolve
    sar "Good evening. Can I get you anything to drink?"
    mc "{i}(Oh, it's Sara, the girl from this morning. Is she really working here?){/i}"
    scene basebar_sara010 with dissolve
    l "Oh, yes please! I'll have a beer"

    scene basebar_sara030 with dissolve
    r "A beer for me as well, thank you."

    scene basebar_sara040 with dissolve
    sar "And for you...sir?"
    mc "Yeah, a beer for me too, please. Thanks."
    sar "Three beers, got it. I'll be right back."

    scene basebartalk010 with dissolve
    l "She seems nice. Do you know her, [player_name]?"
    mc "I, uh, I think I might have seen her around the beach. This is a small village, after all."

    scene mabel_presents010 with dissolve
    mab "Good evening, ladies and gentlemen! And welcome, welcome to our humble establishment! For those of you new to our little slice of paradise, I'm Mabel, your hostess for the evening!"
    mc "{i}(No way. Mabel, the same Mabel from this morning. And while that cocktail dress doesn't leave much to the imagination, it is still a lot more than she'd been wearing just a few hours ago.){/i}"
    scene basebartalk020 with dissolve
    r "Oh, my word! Look at that dress! It's practically indecent!"
    l "Wow. She's... incredible! And that dress! It's so cool! Look at her curves, Mom!"
    r "Lucy! It's far too revealing for a public stage!"

    scene mabel_presents060 with dissolve
    mab "Tonight, we're bringing you an artist who embodies grace, power, and a fiery passion that will leave you breathless! She's a true star, and a dear friend of mine. Give a huge welcome to the one and only, Claudia!"

    play music musica6 loop
    scene black01 with dissolve
    scene basebar100 with dissolve
    pause 1.0
    scene basebar110 with dissolve
    pause 1.0
    scene basebar120 with dissolve

    scene basebar130 with dissolve

    show looping_images

    scene basebartalk020 with dissolve
    r "Oh, for goodness sake! Look at her! She's practically naked! This is disgusting! How can George allow this? My daughter is here!"
    l "Woah... she's got a really nice back, too. And her butt... it's huge! I wonder how she moves like that without falling over."
    scene basebar120 with dissolve
    r "Lucy! Stop staring! She's indecent! And her breasts are... they're just... obscene!"
    scene basebar130 with dissolve
    pause 1.0
    scene basebar140 with dissolve
    pause 1.0
    scene basebar150 with dissolve
    pause 1.0
    scene basebar160 with dissolve
    r "Oh, for heaven's sake! This is absolutely scandalous! Look at her! Those ridiculous little stickers! She's practically nude! I'm going to complain to George about this, [player_name], I really am!"
    scene basebar180 with dissolve
    pause 1.0
    scene basebartalk050 with dissolve
    r "I simply cannot believe this, [player_name]! This is utterly inappropriate! Look at her! It's like a burlesque show, not a family-friendly venue! And Lucy, stop gawking!"
    l "[player_name], did you see that? Wow."

    scene basebar190 with dissolve
    l "She's so good! Like, how does she do that with her boobs? They're like, alive! And she's so confident! I wish I had curves like that!"
    scene basebar200 with dissolve
    pause 1.0
    scene basebar210 with dissolve
    stop music fadeout 1.0
    play sound "Applause.mp3"

    scene basebartalk020 with dissolve
    r "Did you actually enjoy this spectacle, [player_name]? "
    mc "Well, it was... unexpected."

    scene basebarleave with dissolve
    r "Unexpected? It was tasteless! And completely obscene! I cannot believe George brought us here!"
    l "Mom! Don't be so dramatic. It was performance art! It was daring!"
    r "Daring? It was practically pornography! [player_name], Lucy, we are leaving. Right now. I refuse to sit here for another second."
    mc "Rachel, hold on a minute. It was just a performance..."
    r "No! I'm serious. I'm going to find George. He needs to understand how completely inappropriate that was."

    scene basebarleave020 with dissolve
    r "George! I need a word with you, right now!"
    ge "Rachel, my dear! Wasn't Claudia magnificent? Such raw talent, isn't she? The energy she brings to the stage!"

    scene basebarleave030 with dissolve
    r "Magnificent? George, that was not magnificent! That was... that was absolutely not what I expected! It was practically indecent! Did you even {b}see{/b} what she was wearing? Or, rather, what she wasn't wearing?!"
    ge "Wearing? Oh, she looked fantastic! Perfectly suited for the act, wouldn't you say? It's a show bar, Rachel. It's meant to be a bit... extravagant. What's the problem?"

    r "We are leaving. And I'm taking [player_name] and Lucy with me!"

    scene black03 with dissolve
    pause 1.0
    centered "End of Day 2"

    jump day3
    return


################### INTRODUCTION #################################


label introduction:
    ga "You are a middle-aged man. You have just started a relationship with a separated woman named Rachel."
    scene rachel_office02 with dissolve
    ga "You and Rachel have decided that spending some time together on vacation would be a good idea. You rent an apartment in a seaside town for the two of you to stay for a week"
    scene rachel_office01 with dissolve
    ga "But at the last minute, Lucy, Rachel's daughter,  joins as well."
    ga "So, you, Rachel, and her daughter Lucy go to collect the keys for the apartment."
    return



label age_verification_prompt:
    menu:
        "Are you 18 years old or older?"
        "Yes":
            $ age_prompt = True  # Set the variable to True if the user selects "Yes"
        "No":
            $ age_prompt = False  # Keep the variable as False if the user selects "No"

    if age_prompt:
        return  # Continue with the game if age_prompt is True
    else:
        "Sorry, you must be 18 or older to play this game."
        "Goodbye!"
        $ renpy.quit()
        return  # Exit the game



################### DAY 1 #################################

label waiting:
    play music musica5 loop
    scene waiting010 with dissolve
    mc "How long has it been now?"
    r "I don’t know, maybe twenty minutes? They said they'd be here at noon."
    l "It’s twelve thirty."
    mc "Fantastic. We’re just out here baking like we’re part of the scenery."
    scene waiting022 with dissolve
    l "You’d think people who rent out their place would be a little more… punctual."
    mc "You mean responsible?"
    scene waiting021 with dissolve
    r "Alright, let’s not start. Travel delays happen."
    mc "Yeah, but we had to get up at six in the morning to catch that train, and now we’re just..."
    scene waiting024 with dissolve
    l "...left on the curb like abandoned luggage."
    r "Very dramatic."
    mc "But accurate."
    scene waiting020 with dissolve
    r "Let’s just try to stay positive, alright? Maybe they got stuck in traffic."
    l "Maybe they forgot about us."
    scene waiting030 with dissolve
    ge "Hi! So sorry to keep you waiting."
    mc "Lucky us."
    r "Oh, no worries. These things happen. I’m Rachel. And the girl attached to the cellphone is my daughter Lucy"
    scene waiting032 with dissolve
    ge "Rachel! Yes, of course. And you must be ..."
    mc "Yeah, I’m [player_name]"
    ge "Pleasure! I’m George. Claudia, my wife, will be here in a sec. She just had to run back for something. Now, let me just find the... oh, wait, I gave Claudia the keys."
    scene waiting051 with dissolve
    l "Sorry, but I have to leave. My best friend is calling me. See you George"
    ge "See you Lucy. We'll have to wait for my wife, sorry"
    scene waiting071 with dissolve
    c "George, you left without me!"
    ge "Thought I’d get a head start."
    scene waiting072_2 with dissolve
    c "Typical. Hello, hello! So sorry for the wait. I swear, this town is impossible to navigate"
    ge "That’s my wife, Claudia."

    #Transition: from top to bottom in 4 seconds
    scene claudia_full with dissolve:
        xalign 0.0 yalign 1.0 zoom 1
        linear 8.0 yalign 0.0
    pause 8.0
    pause 2.0
    mc "It’s alright, we were just..."
    scene waiting_keys02 with dissolve
    c "Now, where did I put those keys…"
    scene waiting_keys with dissolve
    c "Ah, here!"
    scene waiting140 with dissolve
    c "I won’t be sticking around. I’m off to the beach."
    ge "That's how she is: always running off to the beach"
    scene waiting105 with dissolve
    mc "{i}(Uhm...I think she is not wearing a bikini or swimsuit){/i}"

    scene waiting_pointing with dissolve
    c "The beach is just a tweny-minute walk that way. It's very nice and quiet. You have to go"
    ge "Rather than quiet I'd say solitaire. But I agree, it's very nice."

    scene waiting101 with dissolve
    c "You can’t live this close to the water and not take advantage, can you?. Anyway, enjoy the place!"
    mc "{i}(She is definitely not wearing anything under that top){/i}"

    scene waiting130 with dissolve
    ge "Take care honey."
    play sound "Kiss.mp3"
    c "Yes my love, you too."

    scene waiting160 with dissolve
    c "Oops, the wind blows my skirt"
    mc "{i}(Did she do it on purpose?){/i}"
    scene waiting210 with dissolve
    l "Hey, I'm back!"
    ge "Alright then! The place is all set for you. And you have my number if you need anything. Seriously, anything."
    r "Thank you. We really appreciate it"
    scene waiting220 with dissolve
    r "Ready? let's get moving!"
    l "Yeah, finally..."
    mc "Let's see the apartment, then"
    return

label apartment:
    scene 0rebedor03 with dissolve
    r "Yeah, at least we’re in. And they weren’t wrong about the place: it’s nice."
    l "Well, it's a bit small but it's ok."
    mc "It'll be ok for a week I guess."
    scene 0rebedor05 with dissolve
    l "And what should we do now?"
    r "I don't know, we can start unpacking..."
    mc "You know, the beach does sound pretty good right now."
    scene 0rebedor04 with dissolve
    r "we will unpack first. You can go to the beach if you want"
    l "You are the lucky one, we will be unpacking while you can enjoy the beach withou us"
    mc "Well, I can stay and help, if you want"
    scene 0rebedor06 with dissolve
    r "Don't worry, you can go and afterwards tell us where the beach is"
    l "Remember, no sneak peeks without permission."
    mc "I'll be a good boy, I promise."
    return


label alina:
    play music musica1 loop
    scene tothebeach with dissolve
    mc "{i}(This muste be the way to the beach that Claudia mentioned. I'll check if I can still see her){/i}"
    scene newalina01 with dissolve
    mc "{i}(mmm, nice girl, it seems she is taking selfies alone...){/i}"
    mc "What should I do?"

    menu:
            "Approach her and talk":
                mc "I'll better talk to her"
                scene newalina03 with dissolve
                mc "Hi, could you send me one of these selfies so I can show Santa what I want for Christmas. "
                scene newalina004 with dissolve
                u "Wow, that might be the cheesiest line I’ve heard all week. And I work in marketing, so that’s saying something."
                mc "Cheesy, maybe. But effective? I’ll let you be the judge of that. I’m [player_name], by the way. And you are…?"



            "Wait":
                scene newalina02 with dissolve
                mc "I'll better wait from a safe distance. Maybe I can have a sexy view of her body"
                scene newalina001 with dissolve
                mc "{i}(She's gonna see me anyway soon. I'll better get closer to her){i}"
                scene newalina04 with dissolve
                mc "{i}(She's taking a picture of her tit!){i}"
                scene newalina05 with dissolve
                u "What the hell are you doing? Do you mind? Or do you make a habit of creeping on women who are just trying to enjoy their day?”"
                mc "Whoa, hey. I’m sorry if I made you uncomfortable. I wasn’t trying to creep on you. I was just… admiring the view. You looked like something out of a magazine, and I guess I got a little distracted."
                scene newalina_angry2 with dissolve
                u "Admiring the view, huh? That’s what they all say. You know, it’s not exactly flattering to realize some random guy has been staring at you like you’re a piece of meat."
                mc "Okay, fair point. I didn’t mean it like that, I swear. I just… I don’t know. You looked like you were having fun, and it was kind of infectious. I didn’t mean to ruin your vibe."
                scene alina_talk_02 with dissolve
                u "Alright, you’re lucky. I’m in a decent mood today. But if you’re not a creep, then what are you doing here? Besides ‘admiring the view,’ that is."
                mc "Just taking a walk. Clearing my head. I just arrived today, and there's something about the ocean that helps me unwind. What about you? Are you a professional model, or do you just enjoy taking selfies on the beach?"
                scene newalina21 with dissolve
                u "Neither. I'm just here to enjoy the beach. And maybe get a few good pictures while I'm at it. Though, I have to admit, it's not easy taking a decent selfie with the sun in your eyes."
                mc "Well, if you need a hand, I'd be happy to help. I may not be a professional photographer, but I can at least make sure you're not squinting in every shot. I’m [player_name], by the way. And you are…?"

    scene newalina_kiss with dissolve
    w "Alina. Nice to meet you, [player_name]. Though I’m still not sure if I should be flattered or concerned that you were watching me take selfies."
    mc "Guilty as charged. But in my defense, it’s hard not to notice someone who looks like they just stepped out of a magazine shoot. You’ve got this whole… vibe going on. Very 'effortlessly stunning'"
    scene newalina21 with dissolve
    w "You’re laying it on thick, aren’t you?"
    mc "Only because it’s true. But hey, if you’re not convinced, I’d be happy to prove it. How about I take a few shots for you? I promise I’ll do a better job than your arm."
    scene newalina22 with dissolve
    w "You think you can do better, huh? Alright, hotshot. Let’s see what you’ve got. Here is my cellphone. Just don’t drop it in the sand, or you’re buying me a new one."
    mc "I'll do my best. Alright, just... be natural. Pretend I'm not here."
    scene newalina1002 with dissolve
    w "Easier said than done when you're holding my phone hostage."
    mc "Alright, now let's start with a few natural poses. Turn just a bit. Just be yourself and enjoy the moment."
    scene newalina1003 with dissolve
    w "Okay, I guess I'll try."
    mc "Thanks. I've had a bit of practice. Now, let's get you to face the waves, that way the light will hit your features just right."
    scene newalina1004 with dissolve
    w "Sure, I'll do my best model pose."
    mc "You'd be surprised what you're capable of. Just follow my lead, and we'll create something amazing."
    scene newalina1005 with dissolve
    w "Deal."
    mc "Now, let’s see… how about we start with something a little more… dynamic? Maybe lose the top? You know, give it that ‘model on the beach’ vibe."
    w "Lose the top? Bold move, [player_name]. You don’t waste any time, do you?"
    scene newalina1006 with dissolve
    mc "Hey, I’m just trying to help you get the best shot possible. And let’s be honest, you’d look amazing either way. But if you’re going for that high-fashion, windswept look, a little less fabric might help sell it"
    w "I don't know, I've never done anything like this before."
    scene newalina58 with dissolve
    mc "I want to capture your true essence, your sensuality. It's all about art and expression."
    w "Ok, but pelase, turn around..."
    scene newalina_turn with dissolve
    mc "Take your time."
    w "Ready."
    scene newalina10001 with dissolve
    mc "Great. Now, can you cover your breasts with your hands?"
    scene newalina10 with dissolve
    w "Like this?"
    scene newalina12 with dissolve
    mc "Perfect! Let's get a few more shots."
    w "Alright."
    mc "Now, let’s try something a little more playful. Turn just a bit and laugh like I just told the funniest joke you’ve ever heard."
    scene newalina11 with dissolve
    w "You’re ridiculous."
    mc "And yet, you’re smiling. These are great."
    mc "Let's try now with a picture of you kneeling in the sand."
    scene newalina13 with dissolve
    w "Like this? Happy?"
    mc "That's perfect."
    mc "You know, if you’re comfortable with it, the pictures would look even more stunning without the sarong. The light and your silhouette… it’d be really artistic."
    scene newalina14 with dissolve
    w "Is this really necessary?"
    mc "It's all for the art. And I can tell you're getting more comfortable."
    scene newalina2002 with dissolve
    w "I've never felt so exposed before."
    mc "That's the point. Vulnerability is the most alluring trait."
    w "I guess so."
    scene newalina2004 with dissolve
    mc "This pose is perfect!"
    w "Thanks."
    scene newalina2005 with dissolve
    mc "Let's get a few more shots on the sand"
    w "Sounds good."
    scene newalina2010 with dissolve
    mc "Now, let's get a close-up."
    w "I'm still a bit nervous about this."
    scene newalina2011 with dissolve
    mc "Don't be. You look incredible. The way the light hits your body... it's like you're a sculpture come to life."
    w "Ha ha"
    scene newalina201202 with dissolve
    mc "Just bend over"
    scene newalina2012 with dissolve
    w "Do you like what you see?"
    mc "Sure, let's take it to the next level. The light here is just perfect."
    scene newalina2012_02 with dissolve
    w "What do you mean?"
    mc "Just let the fabric of your bikini bottoms fall away."
    scene newalina2012_03 with dissolve
    w "Oh, I don't know if I'm comfortable with that."
    mc "It's up to you. But remember, it's all about art. Nothing more."
    scene newalina2013 with dissolve
    w "Okay, I'll do it. But only for the sake of the photos. Just don’t get any ideas."
    mc "Thank you. Strictly professional. You're going to be stunning."
    scene newalina14 with dissolve
    w "This is kind of fun, but also a bit nerve-wracking."
    mc "Don't worry, I'm just here to capture your beauty. And you're definitely not disappointing."
    scene newalina42 with dissolve
    w "Ok, It's the first time that I pose totally nude."
    mc "Wow, you're absolutely breathtaking. It'll add an element of nature to the photos."
    scene alinanude01 with dissolve
    w "Are you sure about this? I've never done anything like this before."
    mc "You're stunning. Trust me, these photos will be tasteful and artistic. Just relax and enjoy the moment."
    scene alinanude02 with dissolve
    w "What if someone sees us?"
    mc "Don't worry, we're pretty secluded here."
    scene newalina15 with dissolve
    w "How many more?"
    mc "Just a few. Let's make them count."
    scene newalina16 with dissolve
    w "Okay, but just a few more. I don't want to push my luck."
    mc "That's it. You're a natural."
    scene newalina31 with dissolve
    w "Okay, but I'm getting a bit nervous."
    mc "Look at the camera, like you're telling it your deepest desires."
    scene newalina32 with dissolve
    w "I can't believe I'm doing this."
    mc "You should. You're incredible."
    scene newalina41 with dissolve
    mc "Spread your legs wider."
    scene newalina41_4 with dissolve
    w "It's like you're capturing a secret part of me."
    mc "And what a beautiful secret it is."
    scene newalina09 with dissolve
    mc "Just focus on the sound of the waves and the breeze on your skin. It's just you and the camera."
    w "ok, here I go"
    scene newalina16 with dissolve
    mc "Perfect. You're doing great. Let your inhibitions go with the waves."
    w "You know, you’re not so bad for a stranger on the beach."
    scene newalina28 with dissolve
    mc "And you’re not so bad yourself, Alina"
    scene newalina30 with dissolve
    w "Okay, I think we got enough. Let’s call it a day."
    scene newalina50 with dissolve
    mc "Okay, take a look at those photos, make sure we got some good ones."
    w "Wow, they're... amazing."
    scene newalina51 with dissolve
    mc "Well, I can't promise they'll all be suitable for... public consumption."
    w "These actually turned out amazing. You’ve got a good eye."
    scene newalina56 with dissolve
    mc "(grinning) Told you. The lighting did half the work, though."
    w "You know… if you’re up for it, I wouldn’t mind doing this again sometime. Maybe with a different vibe."
    mc "What’d you have in mind?"
    scene newalina55 with dissolve
    w "So… you up for doing this again sometime? Maybe even a little spicier?"

    menu:
            "yes":
                mc "Sure"
                $lust += 5
                $alina += 5
                #show screen lust5
                scene newalina59 with dissolve
                w "Give me your number, then. I’ll text you so you have mine."
                #stop music fadeout 1.0
                $ renpy.music.set_pause(True, channel="music")
                pause 1.0
                play sound "message.mp3"
                pause 1.0
                $ renpy.music.set_pause(False, channel="music")
                mc "Got it"
                scene newalina57 with dissolve
                w "Alright, I should head out now. But… I’ll hit you up soon."
                mc "(nodding) Looking forward to it."
                scene newalina60 with dissolve
                w "Don’t miss me too much."
                mc "No promises."
            "no":
                mc "Shit, I should’ve mentioned earlier. I’ve actually got a girlfriend."
                scene newalina54 with dissolve
                w "Well, she’s lucky. You’re decent at this."
                mc "Yeah, sorry. Today was fun, but I don’t wanna cross lines."
                scene newalina52 with dissolve
                w "Totally get it. Thanks for being honest. But if you ever break up, you know where to find me."
                mc "Noted. Take care, Alina."
                scene newalina53 with dissolve
                w "You too, [player_name]. Tell your girl she’s got good taste."


    scene newalina_blowingkiss with dissolve:
        xalign 0.0 yalign 1.0 zoom 1
        linear 8.0 yalign 0.0
    pause 8.0
    pause 2.0

    scene gohome with dissolve
    mc "{i}(Well, that was a really weird first day. I'm gonna go see what Rachel and Lucy are up to){/i}"
    return


label night1:
    scene night_apart040 with dissolve
    r "How was your walk? See anything... interesting?"
    mc "Oh, you know. Waves, sand, the usual. Though I did spot a few tiny bikinis."
    scene night_apart010 with dissolve
    r "Oh! Uh... really?"
    mc "Just enjoying the scenery. Though I’ve got the best view right here."
    scene night_apart020 with dissolve
    r "Aw, isn't that sweet..."
    mc "I'll go see what Lucy's up to."
    scene night_apart050 with dissolve
    r "Okay, I'll finish preparing lunch."
    scene night_apart60 with dissolve
    mc "And what’s up, beach goddess? Didn’t melt into the sofa yet?"
    scene night_apart61 with dissolve
    l "So... did you see any hot girls in bikinis? Or was the view back here better?"
    scene night_apart070 with dissolve
    mc "I only saw waves, seagulls, and a stray beach ball. Nothing worth writing home about. Except maybe this apartment’s view."
    l "Smooth recovery. Classic."
    scene night_apart080 with dissolve
    mc "Comfortable?"
    l "Mmm, very. This couch is perfect for lounging. Or… other things."
    mc "Is that so? And what ‘other things’ did you have in mind?"
    scene night_apart100 with dissolve
    l "Oh, you know… watching the sunset, listening to the waves… maybe getting a private recap of your very solo beach walk."
    mc "Private recap, huh? Well, it was a nice walk. Sun, sand, peace and quiet…"
    l "Sounds lonely. You should’ve taken me with you. I’d have made it way more interesting."
    menu:
        "Sneak a peek":
            scene night_apart090 with dissolve
            $lust += 5
            $lucy += 5
            #show screen lust5
            mc "Oh yeah? How so?"
            l "Well, for starters, I wouldn’t have just walked. I’d have made sure you had something way better to look at than just… seagulls."
            mc "Noted. But your mom might have something to say about that."
            scene night_apart091 with dissolve
            l  "Pfft, she’s busy. Besides, I’m way more fun. So… did you really just walk, or did you sneak a peek at some bikini-clad hotties?"
            mc "Wouldn’t you like to know?"
            scene night_apart110 with dissolve
            l "Oh, I definitely would. But I bet none of them looked as good as this."
            mc "Confident, aren’t we?"
            l "Just stating facts. You know I’m the best view in this apartment."
        "Better not":
            scene night_apart120 with dissolve
            mc "{i}(This girl is a little brat...){/i}"
    mc "You’re trouble."
    l "And you love it."
    mc "Alright, I should probably go… help with dinner. Before I accidentally get myself in trouble."
    l "Boring. But fine. "

    scene black01 with dissolve
    centered "After dinner, you all go to bed"

    scene bed_11 with dissolve
    mc "Rachel, babe, you have no idea how much I’ve been thinking about this. Long day, sure, but being here with you? This is what I’ve been waiting for. Let’s make tonight about us. Just you and me, no distractions."
    l "[player_name], I’m… I’m just exhausted. It’s not you, I promise. It’s just… today was so long, and I feel like I’ve been running on empty. I just need to sleep, okay? Can we just… rest? Please?”"
    scene bed_21 with dissolve
    mc "{i} I don’t want to push her, but damn, I want her to know how much she means to me. {/i}"
    scene bed_30 with dissolve
    mc "Alright, babe, I hear you. We’ll rest. No pressure, I promise. But you gotta know, Rachel, you’re the one I’m here with. The only one I’m thinking about right now. We’ve got all the time in the world. Let’s just be here, together."

    scene black01 with dissolve
    centered "End of Day 1"

    return


screen lust10():
     timer 3.0 action Hide()
     text "Lust +10" xpos 0.1 ypos 0.1


screen lust5():
     timer 3.0 action Hide()
     text "Lust +5" xpos 0.1 ypos 0.1

screen lustm5():
     timer 3.0 action Hide()
     text "Lust -5" xpos 0.1 ypos 0.1

screen centered_text_screen(message):
    zorder 100
    frame:
        xalign 0.5 yalign 0.5
        text "[message]" style "centered_text"

style centered_text:
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#ffffff"
    size 36

label show_centered_text:
    call screen centered_text_screen("Hello, World!")
    return
# com utlitzar-ho
#call screen centered_text_screen("bla bla bla.")


image looping_images:
    "image1.webp"
    pause 1.0  # Display first image for 1 second
    "image2.webp"
    pause 1.0  # Display second image for 1 second
    repeat     # Loop indefinitely


