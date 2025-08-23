lang_page_style = """
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center top;
                    color: white;
    
                    /* text centered horizontally; vertical position via padding */
                    padding-top: 20px;      /* space above text */
                    padding-bottom: 36px;   /* reserves space below for the image */
    
                    border: 2px solid #333;   /* constant width → no jump */
                    border-radius: 6px;
                    background-color: rgba(255,255,255,0.04);
    
                    background-image: url("{}");
                    background-repeat: no-repeat;
                    background-origin: content;
                    background-position: center bottom;  /* image sits lower */
                }}
                QPushButton:hover {{
                    border-color: #b0b0b0;                 /* visual cue only */
                    background-color: rgba(255,255,255,0.2);
                }}
            """

level_page_style ="""
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center;
                    color: white;

                    border: 2px solid #333; /* constant width → no jump */
                    border-radius: 6px;
                    background-color: {};
                }}
                QPushButton:hover {{
                    border-color: #b0b0b0; /* visual cue only */
                    background-color: {};
                }}
            """

size_page_style = """
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center top;
                    color: white;

                    /* text centered horizontally; vertical position via padding */
                    padding-top: 20px;      /* space above text */
                    padding-bottom: 36px;   /* reserves space below for the image */

                    border: 2px solid #333;   /* constant width → no jump */
                    border-radius: 6px;
                    background-color: rgba(255,255,255,0.04);

                    background-image: url("{}");
                    background-repeat: no-repeat;
                    background-origin: content;
                    background-position: center bottom;  /* image sits lower */
                }}
                QPushButton:hover {{
                    border-color: #b0b0b0;                 /* visual cue only */
                    background-color: rgba(255,255,255,0.2);
                }}
            """

mode_page_style = """
                    QPushButton {{
                        font-size: 20px;
                        font-weight: bold;
                        text-align: center top;
                        color: white;

                        /* text centered horizontally; vertical position via padding */
                        padding-top: 20px;      /* space above text */
                        padding-bottom: 36px;   /* reserves space below for the image */

                        border: 2px solid #333;   /* constant width → no jump */
                        border-radius: 6px;
                        background-color: rgba(255,255,255,0.04);

                        background-image: url("{}");
                        background-repeat: no-repeat;
                        background-origin: content;
                        background-position: center bottom;  /* image sits lower */
                    }}
                    QPushButton:hover {{
                        border-color: #b0b0b0;                 /* visual cue only */
                        background-color: rgba(255,255,255,0.2);
                    }}
                """