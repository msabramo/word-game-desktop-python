import Dialogs.NameEntryDialog, Utils, datetime, sys, os, os.path
pickle = Utils.import_cPickle_or_pickle()


class TopScoreManager(object):

    def __init__(self):
        self.data_dir = None

    def set_data_dir(self, data_dir):
        self.data_dir = data_dir

    def top_scores_filepath(self):
        filepath = 'top_scores.dat'
        if self.data_dir:
            filepath = self.data_dir + os.path.sep + filepath

        return filepath

    def check_if_top_score(self, score, game, application):
        if score <= 0: return
        
        candidate_entry = (score, game)
        top_scores = self.load_top_scores()
        top_scores.append(candidate_entry)
        top_scores.sort()
        top_scores.reverse()
        top_scores = top_scores[0:10]

        if candidate_entry in top_scores:
            idx = top_scores.index(candidate_entry)
            name = Dialogs.NameEntryDialog.show(application, score, idx)
            if name:
                game.info.update(dict(name=name))
                self.save_top_scores(top_scores)

    def load_top_scores(self):
        top_scores = []

        try:
            top_scores_file = file(self.top_scores_filepath(), 'rb')
        except IOError:
            return top_scores
        
        try:
            print('Loading top scores from %s' % self.top_scores_filepath())
            top_scores = pickle.load(top_scores_file)
            top_scores_file.close()
            sys.stdout.write('Read from top_scores file %s\n'
                             % self.top_scores_filepath())
        except EOFError, e:
            sys.stderr.write('Exception: %s\n' % e)
            top_scores_file.close()
            ret = os.remove(top_scores_file.name)
            sys.stderr.write('Removing corrupt top_score_files => %s\n' % ret)
        
        return top_scores

    def save_top_scores(self, top_scores):
        old_umask = os.umask(0)
        
        try:
            top_scores_file = file(self.top_scores_filepath(), 'wb')
        except IOError:
            sys.stderr.write('Cannot write to top_scores file %s!\n'
                             % self.top_scores_filepath())
            return
        finally:
            os.umask(old_umask)
        
        ret = pickle.dump(top_scores, top_scores_file)
        top_scores_file.close()
        sys.stdout.write('Wrote to top_scores file %s\n'
                         % self.top_scores_filepath())
        return ret
