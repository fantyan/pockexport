#!/usr/bin/env python3
import json

import pocket # type: ignore

class Exporter:
    def __init__(self, *args, **kwargs) -> None:
        self.api = pocket.Pocket(*args, **kwargs)

    def export_json(self):
        # When pocket web app queries api it's got some undocumented parameters, so this small hack allows us to use them too
        # e.g. {"images":1,"videos":1,"tags":1,"rediscovery":1,"annotations":1,"authors":1,"itemTopics":1,"meta":1,"posts":1,"total":1,"state":"unread","offset":0,"sort":"newest","count":24,"forceaccount":1,"locale_lang":"en-US"}
        @pocket.method_wrapper
        def get(self, **kwargs):
            pass

        # apparently no pagination?
        res = get(
            self.api,
            images=1,
            videos=1,
            tags=1,
            rediscovery=1,
            annotations=1,
            authors=1,
            itemOptics=1,
            meta=1,
            posts=1,
            total=1,
            state='all',
            sort='newest',
            forceaccount=1,
        )
        return res[0]


def get_json(**params):
    return Exporter(**params).export_json()


def main():
    from export_helper import setup_parser
    import argparse
    # TODO literate documentation from help
    parser = argparse.ArgumentParser("Export/takeout for your personal pocker data")
    setup_parser(parser=parser, params=['consumer_key', 'access_token'])
    args = parser.parse_args()

    params = args.params
    dumper = args.dumper

    j = get_json(**params)
    js = json.dumps(j, ensure_ascii=False, indent=1)
    dumper(js)


if __name__ == '__main__':
    main()
