class GaryCommand:
    @classmethod
    def reply(cls, text_in):
        if text_in == "hello":
            return "hello!!!"

        if text_in == "hydrogen":
            return "name:hydrogen, proton:1, neutron:0, weight:1"

        if text_in == "H":
            return "name:hydrogen, proton:1, neutron:0, weight:1"
