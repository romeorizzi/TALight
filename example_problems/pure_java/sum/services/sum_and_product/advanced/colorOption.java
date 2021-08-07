/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author UTENTE
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author UTENTE
 */

    public class colorOption
    {
        /**
         * The current String.
         *
         * @var String
         */
        private String string = "";

        /**
         * Reset the hidden flag.
         *
         * @return colorOption
         */
        public colorOption resetHidden()
        {
            return this.resetHidden("");
        }

        /**
         * Reset the hidden flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetHidden(String value)
        {
            this.ansi(Integer.toString(28));
            this.raw(value);

            return this;
        }

        /**
         * Reset the invert colors flag.
         *
         * @return colorOption
         */
        public colorOption resetInvertColors()
        {
            return this.resetInvertColors("");
        }

        /**
         * Reset the hidden flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetInvertColors(String value)
        {
            this.ansi(Integer.toString(27));
            this.raw(value);

            return this;
        }

        /**
         * Reset the blink flag.
         *
         * @return colorOption
         */
        public colorOption resetBlink()
        {
            return this.resetBlink("");
        }

        /**
         * Reset the blink flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetBlink(String value)
        {
            this.ansi(Integer.toString(25));
            this.raw(value);

            return this;
        }

        /**
         * Reset the underline flag.
         *
         * @return colorOption
         */
        public colorOption resetUnderline()
        {
            return this.resetUnderline("");
        }

        /**
         * Reset the underline flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetUnderline(String value)
        {
            this.ansi(Integer.toString(24));
            this.raw(value);

            return this;
        }

        /**
         * Reset the dim flag.
         *
         * @return colorOption
         */
        public colorOption resetDim()
        {
            return this.resetDim("");
        }

        /**
         * Reset the dim flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetDim(String value)
        {
            this.ansi(Integer.toString(22));
            this.raw(value);

            return this;
        }

        /**
         * Reset the bold flag.
         *
         * @return colorOption
         */
        public colorOption resetBold()
        {
            return this.resetBold("");
        }

        /**
         * Reset the bold flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption resetBold(String value)
        {
            this.ansi(Integer.toString(21));
            this.raw(value);

            return this;
        }


        /**
         * Reset to default.
         *
         * @return colorOption
         */
        public colorOption reset()
        {
            return this.reset("");
        }

        /**
         * Reset to default.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption reset(String value)
        {
            this.ansi(Integer.toString(0));
            this.raw(value);

            return this;
        }

        /**
         * Set the hide flag.
         *
         * @return colorOption
         */
        public colorOption hide()
        {
            return this.hide("");
        }

        /**
         * Set the hide flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption hide(String value)
        {
            this.ansi(Integer.toString(8));
            this.raw(value);

            return this;
        }

        /**
         * Set the invert color flag.
         *
         * @return colorOption
         */
        public colorOption invertColor()
        {
            return this.invertColor("");
        }

        /**
         * Set the invert color flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption invertColor(String value)
        {
            this.ansi(Integer.toString(7));
            this.raw(value);

            return this;
        }

        /**
         * Set the blink flag.
         *
         * @return colorOption
         */
        public colorOption blink()
        {
            return this.blink("");
        }

        /**
         * Set the invert flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption blink(String value)
        {
            this.ansi(Integer.toString(5));
            this.raw(value);

            return this;
        }

        /**
         * Set the underline flag.
         *
         * @return colorOption
         */
        public colorOption underline()
        {
            return this.underline("");
        }

        /**
         * Set the underline flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption underline(String value)
        {
            this.ansi(Integer.toString(4));
            this.raw(value);

            return this;
        }

        /**
         * Set the dim flag.
         *
         * @return colorOption
         */
        public colorOption dim()
        {
            return this.dim("");
        }

        /**
         * Set the dim flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption dim(String value)
        {
            this.ansi(Integer.toString(2));
            this.raw(value);

            return this;
        }

        /**
         * Set the bold flag.
         *
         * @return colorOption
         */
        public colorOption bold()
        {
            return this.bold("");
        }

        /**
         * Set the bold flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption bold(String value)
        {
            this.ansi(Integer.toString(1));
            this.raw(value);

            return this;
        }

        /**
         * Set a 16-bit color.
         *
         * @param Color16 color
         *
         * @return colorOption
         */
        public colorOption color16(Color16 color)
        {
            return this.color16(color, "");
        }

        /**
         * Set a 16-bit color.
         *
         * @param Color16 color
         * @param String value
         *
         * @return colorOption
         */
        public colorOption color16(Color16 color, String value)
        {
            this.ansi(Integer.toString(color.getValue()));
            this.raw(value);

            return this;
        }

        /**
         * Set a 256-bit color.
         *
         * @param int color
         *
         * @return colorOption
         */
        public colorOption color256(int color) throws Exception
        {
            return this.color256(color, "");
        }

        /**
         * Set a 256-bit color.
         *
         * @param int color
         * @param String value
         *
         * @return colorOption
         */
        public colorOption color256(int color, String value) throws Exception
        {
            if (color < 0 || color > 256) {
                throw new Exception("Valid 256-bit colors must be within the range of 0 and 256.");
            }

            this.ansi("38;5;" + color);
            this.raw(value);

            return this;
        }

        /**
         * Set a 256-bit background color.
         *
         * @param int color
         *
         * @return colorOption
         */
        public colorOption backgroundColor256(int color) throws Exception
        {
            return this.backgroundColor256(color, "");
        }

        /**
         * Set a 256-bit background color.
         *
         * @param int color
         * @param String value
         *
         * @return colorOption
         */
        public colorOption backgroundColor256(int color, String value) throws Exception
        {
            if (color < 0 || color > 256) {
                throw new Exception("Valid 256-bit colors must be within the range of 0 and 256.");
            }

            this.ansi("48;5;" + color);
            this.raw(value);

            return this;
        }

        /**
         * Appends a raw String.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption raw(String value)
        {
            this.string += value;
            return this;
        }

        /**
         * Add a custom ANSI flag.
         *
         * @param String value
         *
         * @return colorOption
         */
        public colorOption ansi(String value)
        {
            this.string += "\u001b[" + value + "m";
            return this;
        }

        /**
         * Build the final string.
         *
         * @param String value
         *
         * @return colorOption
         */
        @Override
        public String toString()
        {
            this.reset();
            return this.string;
        }
          public enum Color16
        {
            FG_RESET(39),
            FG_BLACK(30),
            FG_RED(31),
            FG_GREEN(32),
            FG_YELLOW(33),
            FG_BLUE(34),
            FG_MAGENTA(35),
            FG_CYAN(36),
            FG_LIGHT_GRAY(37),
            FG_DARK_GRAY(90),
            FG_LIGHT_RED(91),
            FG_LIGHT_GREEN(92),
            FG_LIGHT_YELLOW(93),
            FG_LIGHT_BLUE(94),
            FG_LIGHT_MAGENTA(95),
            FG_LIGHT_CYAN(96),
            FG_WHITE(97),
            BG_RESET(49),
            BG_BLACK(40),
            BG_RED(41),
            BG_GREEN(42),
            BG_YELLOW(43),
            BG_BLUE(44),
            BG_MAGENTA(45),
            BG_CYAN(46),
            BG_LIGHT_GRAY(47),
            BG_DARK_GRAY(100),
            BG_LIGHT_RED(101),
            BG_LIGHT_GREEN(102),
            BG_LIGHT_YELLOW(103),
            BG_LIGHT_BLUE(104),
            BG_LIGHT_MAGENTA(105),
            BG_LIGHT_CYAN(106),
            BG_WHITE(107);

            private int value;
            public int getValue()
            {
                return value;
            }

            Color16(int value)
            {
                this.value = value;
            }
        }
        /**
         * Color16 values.
         */
      
    }

    

  
    