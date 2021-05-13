"""
Sydney Whilden
03/29/2021

Compare total hydrogen along sightlines in Sembach (2003) with my results using
a method the observer could emulate.

"""
import OH_fields as oh
import scaleeverything as se
import matplotlib.pyplot as plt
import sys
from datetime import datetime
oh.yt.funcs.mylog.setLevel(50)

class Sightline:
    def __init__(self, name, nhi, novi):
        self.name = name
        self.nhi = nhi  # neutral hydrogen column density
        self.novi = novi  # O VI column density

# see Sembach (2003) Table 8
Mrk279 = Sightline('Mrk 279', 20.4e18, 4.68e13)
Mrk290 = Sightline('Mrk 290', 94.7e18, 15.8e13)
Mrk501 = Sightline('Mrk 501', 10.7e18, 6.46e13)
Mrk506 = Sightline('Mrk 506', 4.4e18, 11.2e13)
Mrk817 = Sightline('Mrk 817', 32.4e18, 7.59e13)
Mrk876 = Sightline('Mrk 876', 19.9e18, 11.2e13)
PG1259 = Sightline('PG 1259+593', 89.5e18, 5.25e13)
PG1351 = Sightline('PG 1351+640', 59.6e18, 5.68e13)
PG1626 = Sightline('PG 1626+554', 26.9e18, 16.6e13)

lines = [Mrk279, Mrk290, Mrk501, Mrk506, Mrk817, Mrk876, PG1259, PG1351, PG1626]
# list of sightlines

def totalH(sightline, met, ion_frac):
    """
    Basically the formula we use to calculate the hydrogen associated with a
    given ion.

    Parameters:
        sightline (object of a class): a Sightline object
        met (float): metallicity
        ion_frac: ionization fraction O VI/O

    """
    nhi = sightline.nhi
    novi = sightline.novi

    nhii = novi / (met * ion_frac)
    # H = nhii + nhi

    return nhii


if __name__ == "__main__":

    epoch = ""  # initialize

    if len(sys.argv[1]) > 1:  # take command line argument
        epoch = sys.argv[1]

    # run main function from OH_fields.py
    file, time, ds, ad, cut = oh.main(epoch)
    se.main()  # this line only works as long as sembach_met = fox_met
    wfile = open("../../Plots/%s.txt" % (time), 'a')
    wfile.write("\n\n{}".format(datetime.today().ctime()))

    proj_x = ds.proj('OVI_scaled', 'x', data_source=cut)

    # ion frac over whole cloud
    # scaling actually makes no difference here
    all_ovi = oh.np.sum(proj_x['OVI_scaled'])
    # all_ovi = all_ovi[all_ovi != 0]

    all_o = oh.np.sum(proj_x['o_total_scaled'])
    # all_o = all_o[all_o != 0]

    ion_frac = all_ovi / all_o
    print("Ionization fraction O VI/O: {}".format(ion_frac))

    sembach_if = 0.2  # sembach ionization fraction

    # mean scaled metallicity
    all_h = oh.np.sum(proj_x['h_total_number'])
    # all_h = all_h[all_h != 0]

    all_hi = oh.np.sum(proj_x['h_neutral_number'])

    sembach_met = all_o / all_h

    ratio = all_hi / all_ovi
    print("N(H I)/N(O VI): {}".format(ratio))

    H_list = []  # initialize
    sembach_Hlist = []

    for line in lines:
        H = totalH(line, sembach_met, ion_frac)
        sembach_H = totalH(line, sembach_met, sembach_if)
        H_list.append(H)
        sembach_Hlist.append(sembach_H)
        wfile.write("\n\nOur method: {}: {}".format(line.name, H))
        wfile.write("\nSembach method: {}".format(sembach_H))

    log_H = []
    log_sembach_H = []
    for H, sembach_H in zip(H_list, sembach_Hlist):
        log_H.append(oh.np.log10(H))
        log_sembach_H.append(oh.np.log10(sembach_H))

    # make list of line names
    line_names = []
    line_novi = []
    line_nhi = []
    for line in lines:
        line_names.append(line.name)
        line_novi.append(line.novi)
        line_nhi.append(line.nhi)

    # Doing this doesn't make sense. Doesn't give total mass.
    # total_H = oh.np.sum(H_list)
    # wfile.write("\nTotal H: {}".format(total_H))
    # total_H_mass = oh.mHydro * total_H
    # wfile.write("\nTotal H mass: {}".format(total_H_mass))

    # plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 4))
    N = len(lines)
    ind = oh.np.arange(N)
    width = 0.2
    ax.bar(ind, H_list, width, label='Us')
    ax.bar(ind + width, sembach_Hlist, width, label='Sembach')
    ax.bar(ind + 2 * width, line_nhi, width, label='N(H I)')
    # ax.bar(ind, log_H, width, label='Us')
    # ax.bar(ind + width, log_sembach_H, width, label='Sembach')
    ax.set_xticks(ind + 0.5 * width)
    ax.set_xticklabels(line_names)
    ax.set_title('Sembach (2003) sightlines')
    ax.set_yscale('log')
    ax.set_ylabel(r'$N(H\ II)_{O\ VI}\ (cm^{-2})$')
    ax.set_xlabel('Sightlines')
    ax.legend()
    plt.savefig('../../Plots/sembachsightlines.png')
    #
    # # for plotting
    # x = oh.np.arange(0, oh.np.max(line_novi), 1e6)
    # xlog = oh.np.arange(0, oh.np.max(oh.np.log10(line_novi)), 1e6)
    # a, b, c = oh.np.polyfit(line_novi, line_nhi, 2)
    # d, e, f = oh.np.polyfit(oh.np.log10(line_novi), oh.np.log10(line_nhi), 2)
    # y = []
    # ylog = []
    # for x_val in x:
    #     y_val = a * x_val**2 + b * x_val + c
    #     y.append(y_val)
    #
    # for xlog_val in xlog:
    #     ylog_val = d * xlog_val**2 + e * xlog_val + f
    #     ylog.append(ylog_val)
    #
    #
    # fig2, ax2 = plt.subplots(nrows=2, ncols=1)
    # plt.subplots_adjust(
    #     left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5
    #     )
    # ax2[0].scatter(line_novi, line_nhi)
    # ax2[0].plot(x, y, color='r')
    # ax2[0].set_title('N(H I) vs. N(O VI)')
    # ax2[0].set_xlabel('N(O VI)')
    # ax2[0].set_ylabel('N(H I)')
    # ax2[1].scatter(line_novi, line_nhi)
    # # ax2[1].plot(xlog, ylog, color='r')
    # ax2[1].set_yscale('log')
    # ax2[1].set_xscale('log')
    # ax2[1].set_xlabel('N(O VI)')
    # ax2[1].set_ylabel('N(H I)')
    # ax2[1].set_title('N(H I) vs. N(O VI)')
    # fig.tight_layout()
    # plt.savefig('../../Plots/nhi_vs_novi.png')

    # conclude
    wfile.close()
