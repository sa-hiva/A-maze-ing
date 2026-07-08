import curses
from .interface_renderer import safe_addstr


INVALID_KEY_FRAMES = [
    """



          *
       STOP PRESSING INVALID KEYS!!!!




    """,
    """


        ****
        ****
       STOP PRESSING INVALID KEYS!!!!




    """,
    """

       * **
      * *****
      ** * ***
       STOP PRESSING INVALID KEYS!!!!



    """,
    """
        *
      *   ***
     *  ** * *                *
      *      * *
    ** STOP PRESSING INVALID KEYS!!!!
          *


    """,
    """        +
     +    +
            ++              ****
       ++  +  +              ***
   + +        +  +
  +    STOP PRESSING INVALID KEYS!!!!
    + +  +
          +

    """,
    """       oo
    o     o                 *  **
             oo           * *** *
      ooo   o             * **
  o o          oo            ** *
       STOP PRESSING INVALID KEYS!!!!
 o       o  o
   o o
          o
    """,
    """       o  o                *     *
  o          o           *   *  ***
              o             ** * *
      ooo   o           *   *
o  o            oo           * *  *
       STOP PRESSING INVALID KEYS!!!!
        o    o      *
o        o
 o  oo
          o
    """,
    """:     :  :               +       ++
              :        +     +  + +
               :           ++  +
     ::::    :        +
                 :         + +
  :    STOP PRESSING INVALID KEYS!!!!
                  ****      +
        :    :
         :
         :  ::
    """,
    """.         .               o      o  oo
               .     o       o     o
                .          oo  o
    . ..            o
      .      .    **      o
 .     STOP PRESSING INVALID KEYS!!!!o
                 **  ***.      o
        .         ***      o
              .
         .
    """,
    """.         .                       o  oo
               .    o       o       o
                 .        oo    o
    ..           **        o
      ..      .  **
       STOP PRESSING INVALID KEYS!!!!
.               * * .* ***            o
               ******    .      o
        .        * *       o
              .
    """,
    """                                  :   : :
                  :         :        :
                          ::
                + +       ::    :
                + +
       STOP PRESSING INVALID KEYS!!!!
                  +   +  +  ::
              ++ +        +             :
                + +++           :
    """,
    """                                   .     .
                 .          .         .
               o o         .
                         ..      .
              .o o
       STOP PRESSING INVALID KEYS!!!!
                 o    o  .o
             o             oo
            o o o                        .
               o  ooo           .
    """,
    """                                    .     .
              o.            .           .
                 o        .
              o         . .      .
              o  o
       STOP PRESSING INVALID KEYS!!!!
                 o         o
                       o.   o
            o              .. o
           oo   o   o                      .
    """,
    """
             :
                :
             :
              : :
       STOP PRESSING INVALID KEYS!!!!
                :           :
                        :
           :                 :
         : :                    :
    """,
    """             .
                .

             .
             .  .
       STOP PRESSING INVALID KEYS!!!!
                .            .
                .             .
                        .      .
          .                      .
    """,
    """            .
                .

            .
            .   .
      .STOP PRESSING INVALID KEYS!!!!
        .   .   .   .         .
               .               .
                         .
        .                       .
    """,
    """



          *
       STOP PRESSING INVALID KEYS!!!!




    """,
    """


        ****
        ****
       STOP PRESSING INVALID KEYS!!!!




    """,
    """

       * **
      * *****
      ** * ***
       STOP PRESSING INVALID KEYS!!!!



    """,
    """
        *
      *   ***
     *  ** * *                *
      *      * *
    ** STOP PRESSING INVALID KEYS!!!!
          *


    """,
    """        +
     +    +
            ++              ****
       ++  +  +              ***
   + +        +  +
  +    STOP PRESSING INVALID KEYS!!!!
    + +  +
          +

    """,
    """       oo
    o     o                 *  **
             oo           * *** *
      ooo   o             * **
  o o          oo            ** *
       STOP PRESSING INVALID KEYS!!!!
 o       o  o
   o o
          o
    """,
    """       o  o                *     *
  o          o           *   *  ***
              o             ** * *
      ooo   o           *   *
o  o            oo           * *  *
       STOP PRESSING INVALID KEYS!!!!
        o    o      *
o        o
 o  oo
          o
    """,
    """:     :  :               +       ++
              :        +     +  + +
               :           ++  +
     ::::    :        +
                 :         + +
  :    STOP PRESSING INVALID KEYS!!!!
                  ****      +
        :    :
         :
         :  ::
    """,
    """.         .               o      o  oo
               .     o       o     o
                .          oo  o
    . ..            o
      .      .    **      o
 .     STOP PRESSING INVALID KEYS!!!!o
                 **  ***.      o
        .         ***      o
              .
         .
    """,
    """.         .                       o  oo
               .    o       o       o
                 .        oo    o
    ..           **        o
      ..      .  **
       STOP PRESSING INVALID KEYS!!!!
.               * * .* ***            o
               ******    .      o
        .        * *       o
              .
    """,
    """                                  :   : :
                  :         :        :
                          ::
                + +       ::    :
                + +
       STOP PRESSING INVALID KEYS!!!!
                  +   +  +  ::
              ++ +        +             :
                + +++           :
    """,
    """                                   .     .
                 .          .         .
               o o         .
                         ..      .
              .o o
       STOP PRESSING INVALID KEYS!!!!
                 o    o  .o
             o             oo
            o o o                        .
               o  ooo           .
    """,
    """                                    .     .
              o.            .           .
                 o        .
              o         . .      .
              o  o
       STOP PRESSING INVALID KEYS!!!!
                 o         o
                       o.   o
            o              .. o
           oo   o   o                      .
    """,
    """
             :
                :
             :
              : :
       STOP PRESSING INVALID KEYS!!!!
                :           :
                        :
           :                 :
         : :                    :
    """,
    """             .
                .

             .
             .  .
       STOP PRESSING INVALID KEYS!!!!
                .            .
                .             .
                        .      .
          .                      .
    """,
    """            .
                .

            .
            .   .
      .STOP PRESSING INVALID KEYS!!!!
        .   .   .   .         .
               .               .
                         .
        .                       .
    """,
]


def animate_invalid_key_spam(stdscr) -> None:
    """Animates each frame from INVALID_KEY_FRAMES"""

    stdscr.nodelay(True)  # Stop listening to keys while animating
    for frame in INVALID_KEY_FRAMES:
        stdscr.erase()
        for row, line in enumerate(frame.split("\n")):
            safe_addstr(stdscr, row, 0, line)
        stdscr.refresh()
        curses.napms(80)

    curses.flushinp()
    stdscr.nodelay(False)
