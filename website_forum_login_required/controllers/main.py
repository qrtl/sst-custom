# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http

from odoo.addons.website_forum.controllers.main import WebsiteForum


class WebsiteForum(WebsiteForum):
    @http.route(["/forum"], type="http", auth="user", website=True)
    def forum(self, **kwargs):
        return super(WebsiteForum, self).forum(**kwargs)

    @http.route(
        [
            '/forum/<model("forum.forum"):forum>',
            '/forum/<model("forum.forum"):forum>/page/<int:page>',
            """/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions""",  # noqa
            """/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions/page/<int:page>""",  # noqa
        ],
        type="http",
        auth="user",
        website=True,
        sitemap=WebsiteForum.sitemap_forum,
    )
    def questions(
        self,
        forum,
        tag=None,
        page=1,
        filters="all",
        sorting=None,
        search="",
        post_type=None,
        **post
    ):
        return super(WebsiteForum, self).questions(
            forum,
            tag=tag,
            page=page,
            filters=filters,
            sorting=sorting,
            search=search,
            post_type=post_type,
            **post
        )

    @http.route(
        [
            """/forum/<model("forum.forum"):forum>/question/<model("forum.post", "[('forum_id','=',forum[0]),('parent_id','=',False),('can_view', '=', True)]"):question>"""  # noqa
        ],
        type="http",
        auth="user",
        website=True,
    )
    def question(self, forum, question, **post):
        return super(WebsiteForum, self).question(forum, question, **post)

    @http.route(
        '/forum/<model("forum.forum"):forum>/badge',
        type="http",
        auth="user",
        website=True,
    )
    def badges(self, forum, **searches):
        return super(WebsiteForum, self).badges(forum, **searches)

    @http.route(
        [
            '/forum/<model("forum.forum"):forum>/tag',
            '/forum/<model("forum.forum"):forum>/tag/<string:tag_char>',
        ],
        type="http",
        auth="user",
        website=True,
        sitemap=False,
    )
    def tags(self, forum, tag_char=None, **post):
        return super(WebsiteForum, self).tags(forum, tag_char=tag_char, **post)

    @http.route(
        ['/forum/<model("forum.forum"):forum>/user/<int:user_id>'],
        type="http",
        auth="user",
        website=True,
    )
    def open_user(self, forum, user_id=0, **post):
        return super(WebsiteForum, self).open_user(forum, user_id=user_id, **post)

    @http.route(
        ['/forum/<model("forum.forum"):forum>/partner/<int:partner_id>'],
        type="http",
        auth="user",
        website=True,
    )
    def open_partner(self, forum, partner_id=0, **post):
        return super(WebsiteForum, self).open_partner(
            forum, partner_id=partner_id, **post
        )

    @http.route(
        ["/forum/user/<int:user_id>/avatar"],
        type="http",
        auth="user",
        website=True,
        sitemap=False,
    )
    def user_avatar(self, user_id=0, **post):
        return super(WebsiteForum, self).user_avatar(user_id=user_id, **post)

    @http.route(
        [
            '/forum/<model("forum.forum"):forum>/users',
            '/forum/<model("forum.forum"):forum>/users/page/<int:page>',
        ],
        type="http",
        auth="user",
        website=True,
    )
    def users(self, forum, page=1, **searches):
        return super(WebsiteForum, self).users(forum, page=page, **searches)

    @http.route(
        ['/forum/<model("forum.forum"):forum>/faq'],
        type="http",
        auth="user",
        website=True,
    )
    def forum_faq(self, forum, **post):
        return super(WebsiteForum, self).forum_faq(forum, **post)
