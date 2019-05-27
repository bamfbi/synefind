from wav_object import *
import glob


def train(
    sample_prefix="samples/Bass*",
    savename=None,
    window_size=100,
    epochs=10,
    batch_size=1,
    neck_dim=32,
    intermediate_dims=[250, 90],
    validation_split=0.2,
    load_if_possible=True,
    ):
    fnames = glob.glob(".data/{}".format(sample_prefix))
    wavs = [wav(f) for f in fnames]

    if savename is None:
        savename = sample_prefix.split('/')[-1].replace('*','')
    if not os.path.exists(savename):
        os.mkdir(savename)

    stacked, index = wav.prepare_multiple(wavs, window_size=window_size)
    ret = autoencode(
        data=stacked.T,
        name=savename,
        epochs=epochs,
        batch_size=batch_size,
        neck_dim=neck_dim,
        intermediate_dims=intermediate_dims,
        validation_split=validation_split,
        load_if_possible=load_if_possible
    )

    reps = ret["encoder"].predict(stacked.T)
    recon = ret["decoder"].predict(reps).T

    wavs_recon = wav.reconstruct_multiple(recon, index)
    wavs_recon[4].write("{}/output".format(savename))
    wavs[4].write("{}/input".format(savename))
    locals().update(ret)
    return locals()

def wav_from_rep(
    rep,
    decoder,
    length=2,
):
    if len(rep.shape) < 2:
        rep = np.asarray([rep])
    n_samples = int(wav.DEFAULT_SAMPLE_RATE*length)
    proc = np.asarray(np.split(decoder.predict(rep).squeeze(), 2))
    proc = (proc[0] + 1j*proc[1])
    proc = np.repeat(np.asarray([proc]), int(n_samples/proc.size), axis=0)
    return wav(istft(proc, fs=wav.DEFAULT_SAMPLE_RATE)[1])
