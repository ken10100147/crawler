"""
search

http://www.zhihu.com/search_v3?content_length=150&correction=1&q=%E7%8E%8B%E5%98%89%E5%B0%94&limit=10&t=general&offset=0&topic_filter=0

zhihu api
https://www.zhihu.com/api/v4/questions/22212644/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=3

https://api.zhihu.com/search?excerpt_len=75&q=%E8%83%B8%E5%A4%A7&t=content

http://www.zhihu.com/api/v4/search_v3?content_length=150&correction=1&search_hash_id=b9e3cef9d346eefe4ae02276983c5fb3&q=%E7%8E%8B%E5%98%89%E5%B0%94&limit=50&t=general&offset=50&topic_filter=0
https://www.zhihu.com/api/v4/search_v3?content_length=150&correction=1&search_hash_id=b9e3cef9d346eefe4ae02276983c5fb3&q=%E7%8E%8B%E5%98%89%E5%B0%94&limit=50&t=general&offset=50&topic_filter=0

    # https://api.zhihu.com/search?content_length=150&correction=0&search_hash_id=1b1214b2848023aa90fdf1cf45b57ce5&q=%E7%8E%8B%E5%98%89%E5%B0%94&limit=10&t=content&offset=10&topic_filter=0
    # https://api.zhihu.com/articles/24066984
    # https://api.zhihu.com/questions/40670407
    # https://www.zhihu.com/api/v4/questions/40670407
    # https://api.zhihu.com/topics/20028217
    # https://www.zhihu.com/api/v4/topics/20028217
    # https://api.zhihu.com/topics/20028217/followers
    # https://www.zhihu.com/api/v4/topics/20028217/followers
    # https://api.zhihu.com/people/brucenoppojeff
    https://www.zhihu.com/api/v4/members/excited-vczh?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics
    https://www.zhihu.com/api/v4/members/brucenoppojeff

https://www.zhihu.com/api/v4/questions/40670407/answers?limit=20&offset=0&sort_by=default&include=data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,collapsed_counts,reviewing_comments_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[].author.is_blocking,is_blocked,is_followed,voteup_count,message_thread_token,badge[?(type=best_answerer)].topics
"""
