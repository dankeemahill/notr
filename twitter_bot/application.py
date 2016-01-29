from PIL import Image, ImageDraw, ImageFont
from twython import Twython, TwythonStreamer
from StringIO import StringIO

import csv
import os
import random


class NotrStreamer(TwythonStreamer):

    def on_success(self, data):
        if "event" in data:
            if data["event"] == "follow":
                twitter = Twython(TWITTER_CONSUMER_KEY,
                                  TWITTER_CONSUMER_SECRET,
                                  TWITTER_ACCESS_TOKEN,
                                  TWITTER_ACCESS_TOKEN_SECRET)

                tweet_data = self.get_tweet(data["source"])

                self.post_tweet(twitter, tweet_data)

    def on_error(self, status_code, data):
        print status_code

    def write_tweet(self, data, screen_name):
        reason_map = {
            "H": "a moving violation",
            "V": "an equipment violation",
            "N": "a non-moving violation",
            "C": "a collision",
            "I": "an investigation",
            "E": "based on information we have",
            "O": "a criminal offense",
            "M": "motorist assistance"
        }

        reason = reason_map[data["reason_for_stop"]]

        prefix = (
            "I stopped your",
            "I pulled over your",
        )[random.randint(0, 1)]

        if "SP" in data["violations_observed"]:
            reason = "speeding"
        elif "FS" in data["violations_observed"]:
            reason = (
                "failing to stop",
                "not stopping"
            )[random.randint(0, 1)]
        elif "TS" in data["violations_observed"]:
            reason = (
                "a turn signal violation",
                "not signaling your turn",
                "not using your turn signal"
            )[random.randint(0, 2)]
        elif "FY" in data["violations_observed"]:
            reason = (
                "failing to yield",
                "not yielding"
            )[random.randint(0, 1)]
        elif "FD" in data["violations_observed"]:
            reason = "following too closely"

        outcome = None
        if "AR" in data["outcome_of_stop"]:
            outcome = " You're under arrest."
        elif "CI" in data["outcome_of_stop"]:
            outcome = " I'm giving you a citation."
            outcome = (
                " I'm giving you a citation.",
                " This is a citation.",
                " Here's a citation."
            )[random.randint(0, 2)]
        elif "WA" in data["outcome_of_stop"]:
            outcome = (
                " I'm giving you a warning.",
                " This is a warning."
            )[random.randint(0, 1)]

        disposition = None
        if data["uda_disposition"].strip() == "RELEASED":
            disposition = (
                " You're released.",
                " You can go."
            )[random.randint(0, 1)]
        elif data["uda_disposition"].strip() == "ICE/CBP":
            disposition = (
                " I'm transferring you to the feds.",
                " You're being transferred to the feds.",
                " I've contacted the feds.",
                " I've contacted border patrol."
            )[random.randint(0, 2)]

        uda_disp = ""
        if outcome:
            uda_disp += outcome
        if disposition:
            uda_disp += disposition

        txt = "@{screen_name} {prefix} {car} for {reason}.{uda_disp}".format(
            prefix=prefix,
            screen_name=screen_name,
            car=data["vehicle_style"],
            reason=reason,
            uda_disp=uda_disp
        )

        if reason == "a collision":
            txt = "@{screen_name} Your {car} was in a collision.{uda_disp}".format(
                screen_name=screen_name,
                car=data["vehicle_style"],
                uda_disp=uda_disp
            )

        if len(txt) > 120:
            txt = "@{screen_name} {prefix} {car} for {reason}.".format(
                prefix=prefix,
                screen_name=screen_name,
                car=data["vehicle_style"],
                reason=reason
            )

        return txt

    def format_name(self, name_data):
        split_name = name_data.split(" ")
        if len(split_name) == 2:
            return [split_name[0], "", split_name[1]]
        elif len(split_name) == 1:
            return [split_name[0], "", ""]
        elif len(split_name) > 2:
            return [split_name[0], split_name[1],
                    " ".join(split_name[2:])]
        else:
            return ["", "", ""]

    def get_tweet(self, source_data):
        font_path = os.environ.get("FONT_PATH")
        base = Image.open("sia_edit.png").convert("RGBA")
        fnt = ImageFont.truetype(font_path, size=20)
        exp_fnt = ImageFont.truetype(font_path, size=25)

        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        options = {
            "font": fnt,
            "fill": (7, 56, 103, 255)
        }

        exp_options = {
            "font": exp_fnt,
            "fill": (7, 56, 103, 255)
        }

        name_data = self.format_name(source_data["name"])

        d.text((140, 317), name_data[0], **options)
        d.text((436, 317), name_data[1], **options)
        d.text((730, 317), name_data[2], **options)

        reader = csv.DictReader(open("bot_data.csv"))

        [reader.next() for i in range(0, random.randint(1, 1750))]
        data = reader.next()

        tweet_text = self.write_tweet(data, source_data["screen_name"])

        d.text((859, 199), data["dateofstop"], **options)
        d.text((1030, 199), data["timeofstop"], **options)
        d.text((116, 248), data["diroftravel"], **options)
        d.text((224, 248), data["onhighway"], **options)
        d.text((328, 248), data["highway_x"], **options)
        d.text((407, 248), data["milepost_x"], **options)
        d.text((496, 248), data["ramp_x"], **options)
        d.text((572, 248), data["otherlocation"], **options)
        d.text((140, 369), data["statuschkrequesttime"], **options)
        d.text((360, 369), data["statuschkrequesttime"], **options)
        d.text((567, 369), data["response"], **options)
        d.text((879, 369), data["country"], **options)

        status_y = 531
        status = data["statuschkexplain"]

        words = status.split(" ")
        word_lines = []

        cur_string = ""
        for word in words:
            if len(cur_string) + len(word) > 65:
                word_lines.append(cur_string)
                cur_string = ""
            cur_string += "{} ".format(word)
        word_lines.append(cur_string)

        for i, line in enumerate(word_lines):
            d.text((117, status_y + (i * 30)), line, **exp_options)

        d.text((116, 1452), "Officer 1070", **options)
        d.text((468, 1452), "1070", **options)

        d.text((701, 1452), "Supervisor 1070", **options)
        d.text((1051, 1452), "1071", **options)

        out = Image.alpha_composite(base, txt)

        return {"img": out, "text": tweet_text}

    def post_tweet(self, twitter, tweet_data):
        image = tweet_data["img"]
        tweet_text = tweet_data["text"]

        image_io = StringIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)

        response = twitter.upload_media(media=image_io)
        twitter.update_status(status=tweet_text,
                              media_ids=[response['media_id']])


if __name__ == "__main__":
    TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    streamer = NotrStreamer(TWITTER_CONSUMER_KEY,
                            TWITTER_CONSUMER_SECRET,
                            TWITTER_ACCESS_TOKEN,
                            TWITTER_ACCESS_TOKEN_SECRET)

    streamer.user()
