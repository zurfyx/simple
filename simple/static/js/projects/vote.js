(function($) {
    /* upvote downvote functionality */

    const PROJECT_ID = $('#project_id').val();

    const UPVOTE_URL = '/projects/' + PROJECT_ID + '/vote/up'
    const UPVOTE_BTN = $('.like-btn');
    const UPVOTES_RESULT = $('.likes-res');

    const DOWNVOTE_URL = '/projects/' + PROJECT_ID +'/vote/down'
    const DOWNVOTE_BTN = $('.dislike-btn');
    const DOWNVOTES_RESULT = $('.dislikes-res');

    const BTN_SELECTED_CLASS = 'selected';

    class UpdateLabels {
        static constants() {
            return {
                ACTION_UPVOTE: 1,
                ACTION_DOWNVOTE: 2
            };
        }

        static update(upvotes='', downvotes='', action) {
            UPVOTE_BTN.removeClass(BTN_SELECTED_CLASS);
            DOWNVOTE_BTN.removeClass(BTN_SELECTED_CLASS);

            UPVOTES_RESULT.text(upvotes);
            DOWNVOTES_RESULT.text(downvotes);

            if (action === UpdateLabels.constants().ACTION_UPVOTE) {
                UPVOTE_BTN.addClass(BTN_SELECTED_CLASS);
            } else if (action === UpdateLabels.constants().ACTION_DOWNVOTE) {
                DOWNVOTE_BTN.addClass(BTN_SELECTED_CLASS);
            }
        };
    }

    ///

    UPVOTE_BTN.click(function() {
        $.post(UPVOTE_URL, function(data) {
            UpdateLabels.update(data.upvotes,
                                data.downvotes,
                                UpdateLabels.constants().ACTION_UPVOTE)
        });
    });

    DOWNVOTE_BTN.click(function() {
        $.post(DOWNVOTE_URL, function(data) {
            UpdateLabels.update(data.upvotes,
                                data.downvotes,
                                UpdateLabels.constants().ACTION_DOWNVOTE)
        });
    });

})(jQuery);