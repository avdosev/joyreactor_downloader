import json
import requests


__query = "query TagPageQuery(\n  $name: String!\n  $lineType: BlogLineType!\n  $favoriteType: BlogLineType\n  $page: Int\n  $isAuthorised: Boolean!\n  $isHomepage: Boolean!\n) {\n  blog(name: $name) {\n    id\n    tag\n    mainBlog {\n      id\n      nsfw\n      unsafe\n      synonyms\n      count\n      name\n    }\n    count\n    postPager(type: $lineType, favoriteType: $favoriteType) {\n      count\n      id\n    }\n    category {\n      tag\n      unsafe\n      nsfw\n      id\n    }\n    ...TagHeader_blog @skip(if: $isHomepage)\n    ...TagSidebar_blog @skip(if: $isHomepage)\n    ...TagPostPager_blog_3OSKdM\n  }\n}\n\nfragment AttributeEmbed_attribute on AttributeEmbed {\n  __isAttributeEmbed: __typename\n  type\n  value\n  image {\n    comment\n    id\n  }\n}\n\nfragment AttributePicture_attribute on AttributePicture {\n  __isAttributePicture: __typename\n  id\n  type\n  insertId\n  image {\n    width\n    height\n    type\n    comment\n    hasVideo\n    id\n  }\n}\n\nfragment AttributePicture_post on Post {\n  nsfw\n  blogs {\n    tag\n    name\n    synonyms\n    id\n  }\n}\n\nfragment Attribute_attribute on Attribute {\n  __isAttribute: __typename\n  type\n  ...AttributePicture_attribute\n  ...AttributeEmbed_attribute\n}\n\nfragment Attribute_post on Post {\n  ...AttributePicture_post\n}\n\nfragment BlogDescription_blog on Blog {\n  id\n  articlePost {\n    ...Content_post\n    ...Content_content\n    id\n  }\n}\n\nfragment CommentTree_comments_2lIf9C on Comment {\n  id\n  level\n  parent {\n    __typename\n    id\n  }\n  ...Comment_comment_2lIf9C\n}\n\nfragment CommentTree_post on Post {\n  id\n  ...Comment_post\n}\n\nfragment CommentVote_comment on Comment {\n  id\n  rating\n  vote {\n    id\n    createdAt\n    power\n  }\n}\n\nfragment Comment_comment_2lIf9C on Comment {\n  id\n  parent {\n    __typename\n    id\n  }\n  user {\n    id\n    username\n  }\n  createdAt\n  rating\n  level\n  ...Content_content\n  ...CommentVote_comment @include(if: $isAuthorised)\n}\n\nfragment Comment_post on Post {\n  id\n  ...Content_post\n}\n\nfragment Content_content on Content {\n  __isContent: __typename\n  text\n  attributes {\n    __typename\n    id\n    insertId\n    ...Attribute_attribute\n  }\n}\n\nfragment Content_post on Post {\n  ...Attribute_post\n}\n\nfragment Poll_post_2lIf9C on Post {\n  id\n  poll {\n    question\n    answers {\n      id\n      answer\n      count\n    }\n    pollVote @include(if: $isAuthorised)\n  }\n}\n\nfragment PostFooter_post_2lIf9C on Post {\n  id\n  commentsCount\n  rating\n  createdAt\n  favorite @include(if: $isAuthorised)\n  ...PostVote_post @include(if: $isAuthorised)\n}\n\nfragment PostPager_posts_3OSKdM on PostPager {\n  posts(page: $page) {\n    id\n    nsfw\n    unsafe\n    blogs {\n      mainBlog {\n        id\n        nsfw\n        unsafe\n      }\n      id\n    }\n    user {\n      username\n      id\n    }\n    ...Post_post_2lIf9C\n  }\n  count\n  id\n}\n\nfragment PostVote_post on Post {\n  id\n  rating\n  minusThreshold\n  vote {\n    id\n    createdAt\n    power\n  }\n}\n\nfragment Post_post_2lIf9C on Post {\n  id\n  user {\n    id\n    username\n  }\n  blogs {\n    tag\n    name\n    showAsCategory\n    id\n  }\n  bestComments {\n    ...CommentTree_comments_2lIf9C\n    id\n  }\n  nsfw\n  unsafe\n  createdAt\n  text\n  favorite @include(if: $isAuthorised)\n  ...PostVote_post @include(if: $isAuthorised)\n  poll {\n    question\n  }\n  ...Content_post\n  ...Content_content\n  ...PostFooter_post_2lIf9C\n  ...CommentTree_post\n  ...Poll_post_2lIf9C\n}\n\nfragment TagHeader_blog on Blog {\n  id\n  name\n  tag\n  synonyms\n  subscribers\n  nsfw\n  unsafe\n  count\n  image {\n    id\n  }\n  mainBlog {\n    id\n    unsafe\n    nsfw\n    articlePost {\n      id\n    }\n    ...BlogDescription_blog\n    subBlogsMenu {\n      ...TagList_blogs\n      id\n    }\n    subBlogs {\n      ...TagList_blogs\n      id\n    }\n    ...TagSuperBlogs_blog\n  }\n  ...TagSidebar_blog\n  articleImage {\n    id\n    type\n  }\n  category {\n    id\n    tag\n    category {\n      id\n    }\n    showAsCategory\n    nsfw\n    unsafe\n  }\n}\n\nfragment TagList_blogs on Blog {\n  id\n  tag\n  name\n  nsfw\n  unsafe\n  count\n  subscribers\n  showAsCategory\n}\n\nfragment TagPostPager_blog_3OSKdM on Blog {\n  id\n  postPager(type: $lineType, favoriteType: $favoriteType) {\n    ...PostPager_posts_3OSKdM\n    count\n    id\n  }\n}\n\nfragment TagSidebar_blog on Blog {\n  tag\n  mainBlog {\n    subBlogsMenu {\n      id\n    }\n    subBlogs {\n      ...TagList_blogs\n      id\n    }\n    ...TagSuperBlogs_blog\n    nsfw\n    unsafe\n    id\n  }\n  category {\n    id\n    tag\n    category {\n      id\n    }\n    nsfw\n    unsafe\n  }\n}\n\nfragment TagSuperBlogs_blog on Blog {\n  subBlogsMenu {\n    id\n    tag\n    nsfw\n    unsafe\n    showAsCategory\n  }\n}\n"


def get_tag_page(tag: str, page: int = 1):
    url = 'https://api.joyreactor.cc/graphql'
    query_json = {
        'query': __query,
        'variables': {
            "name": tag,
            "page": page,
            "lineType": "GOOD",
            "isAuthorised": True,
            "isHomepage": False
        },
    }
    headers = {}
    r = requests.post(url=url, json=query_json, headers=headers)
    return json.loads(r.text)


def extract_main_info(j, log=False):
    if log: print(json.dumps(j, ensure_ascii=False, indent=2))
    return {
        'pages':  round(j['data']['blog']['postPager']['count'] / 10),
        'posts': [
            {
                'id': post['id'],
                'tags': [blog['tag'] for blog in post['blogs']]
            } for post in j['data']['blog']['postPager']['posts']
        ],
    }
