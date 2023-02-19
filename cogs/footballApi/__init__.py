from .footballApi import FootballAPI

def setup(bot):
    bot.add_cog(FootballAPI(bot))